
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 
from pydantic import BaseModel

from fastapi import HTTPException


#Clase para cubrir el crud básico de cualquier modelo

class SQLAlchemyRepositoryCRUD():
    #Iniciamos el modelo y la session
    def __init__(self, session:AsyncSession, item):
        self.session=session
        self.item=item

    #Funcion para obtener una instancia por su id
    async def get_by_id(self,object_id: int):
        stmt=select(self.item).where(self.item.id==object_id)
        result=await self.session.execute(stmt)
        object=result.scalar_one_or_none()
        if not object:
            raise HTTPException(status_code=404, detail="File not found")
        return object

    #Funcion para obtener todas las instancias del modelo
    async def get_all(self):
        stmt=select(self.item)
        result=await self.session.execute(stmt)
        objects=result.scalars().all()
        
            
        return objects
    
    #Funcion para actualizar una instancia
    async def update(self,object_id:int,new_object):
        objeto=await self.get_by_id(object_id)
        data=new_object.model_dump(exclude_none=True)
        for key, value in data.items():
            setattr(objeto,key,value)
        try:
            
            await self.session.commit()
            await self.session.refresh(objeto)
            

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        return objeto

    #Funcion para eliminar una instancia
    
    async def delete(self, object_id: int)->None:
        objeto=await self.get_by_id(object_id)
        if not objeto:
            raise HTTPException(status_code=404, detail=f"{self.item.name} no encontrado")
        try:
            await self.session.delete(objeto)
            await self.session.commit()
        except  Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


    #Funcion para crear una instancia nueva
    async def create(self, object:BaseModel):
        
        data=object.model_dump(exclude_none=True)
        new_object=self.item(**data)
        
        try:
            self.session.add(new_object)
            await self.session.commit()
            await self.session.refresh(new_object)
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        
        return new_object

