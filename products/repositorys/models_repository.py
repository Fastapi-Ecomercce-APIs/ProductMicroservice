from .repository import SQLAlchemyRepositoryCRUD
from models import Product, Category
from sqlalchemy import and_
from schemas import ProductCreate

from sqlalchemy import select
from fastapi import HTTPException


class ProductService(SQLAlchemyRepositoryCRUD):

    async def create(self, new_object:ProductCreate):
        
        data=new_object.model_dump(exclude_none=True)
        product=Product(**data)
        stmt=select(Category).where(Category.id==new_object.category_id)
        result=await self.session.execute(stmt)
        category=result.scalar_one_or_none()
        if not category:
            raise HTTPException(status_code=404, detail=f"No hay ninguna categoria con ese id, debe crearla antes")
        
        try:
            self.session.add(product)
            await self.session.commit()
            await self.session.refresh(product)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
        return product

    async def get_by_category(self, category_id: int):
        stmt=select(Product).where(Product.category_id==category_id)

        result= await self.session.execute(stmt)
        productos= result.scalars().all()
        if not productos:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return productos
    
    async def get_by_filters(self,nombre:str=None, precio_min:int=None, precio_max:int=None, category_id:int =None):
        
        filters=[]
        if nombre:
            filters.append(Product.nombre.ilike(f"%{nombre}%"))
        if category_id:
            filters.append(Product.category_id==category_id)
        if precio_min:
            filters.append(Product.precio>precio_min)
        if precio_max:
            filters.append(Product.precio<precio_max)
        
        
        
        stmt=select(Product)
        if filters:
            stmt=stmt.where(and_(*filters))
        result= await self.session.execute(stmt)
        productos=result.scalars().all()
        
        
        return productos

class CategoryRepository(SQLAlchemyRepositoryCRUD):
    pass

