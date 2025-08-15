from database import Base
from sqlalchemy import Integer, String, DateTime,Column, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime


class Category(Base):
    __tablename__="Categories"
    id=Column(Integer, index=True, primary_key=True, autoincrement=True,unique=True)
    nombre=Column(String, index=True)
    #Definimos su relacion con productos
    productos=relationship("Product", back_populates="categoria")


class Product(Base):
    __tablename__="Productos"

    id=Column(Integer, index=True, primary_key=True, autoincrement=True,unique=True)
    nombre=Column(String, index=True, nullable=False)
    descripcion=Column(String)
    fecha_salida=Column(DateTime, default=datetime.now)
    precio=Column(Float)
    imagen=Column(String)

    category_id=Column(Integer, ForeignKey("Categories.id"),nullable=False)
    categoria=relationship("Category", back_populates="productos")

