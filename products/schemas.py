from pydantic import BaseModel, Field,model_validator
from typing import Optional,List

#Modelo para crear producto
class ProductCreate(BaseModel):
    nombre: str=Field(...,
                    max_length=200)
    descripcion: Optional[str]=Field(default=None, max_length=1000, description="La descripicion del producto ")
    precio: float=Field(...,gt=0)
    imagen:Optional[str]=None
    category_id: int=Field(...)

#Modelo para enviar al cliente
class ProductoSend(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]=None
    precio: float
    imagen:Optional[str]=None
    category_id:int
    
    class Config:
        from_attributes=True


#Modelo para enviar varios productos al cliente
class ProductsSend(BaseModel):
    total_items:int
    pages:int
    current_page:int
    items:List[ProductoSend]

#Modelo para actualizar
class ProductUpdate(ProductCreate):
    pass

#Definimos un modelo para actualizaciones parciales
class PartialProductUpdate(BaseModel):
    nombre: Optional[str]=None
    descripcion: Optional[str]=None
    precio: Optional[float]=None
    imagen:Optional[str]=None
    category_id: Optional[int]=None

#Modelo para buscar por filtros
class ProductFilter(BaseModel):
    nombre: Optional[str]=None

    precio_max: Optional[int]=None
    precio_min:Optional[int]=None
    
    category_id: Optional[int]=None

    @model_validator(mode="after")
    def prices_validation(self):
        if self.precio_min is not None and self.precio_max is not  None:
            if self.precio_min>self.precio_max or self.precio_max<self.precio_min:
                raise ValueError(f"Algo anda mal con los precios introducidos")


# Modelo para crear una categoria
class CategoryCreate(BaseModel):
    nombre:str=Field(..., 
                max_length=300)
    

class CategoryUpdate(CategoryCreate):
    pass

class CategorySend(BaseModel):
    id:int
    nombre:str

    class Config:
        from_attributes=True
