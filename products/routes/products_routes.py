from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.responses import Response, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import database, models, schemas
from repositorys import models_repository
from typing import List, Optional



#Funcion para obtener la session como dependencia
def get_db(db:AsyncSession=Depends(database.get_session)):
    return  db

#Funcion para obtener ProductService como dependencia

def get_product_service(session:AsyncSession=Depends(get_db)):
    return models_repository.ProductService(session,models.Product )

router=APIRouter(prefix="/products", tags=["Products"])



#Ruta para crear un producto

@router.post("/create", response_model=schemas.ProductoSend, status_code=status.HTTP_201_CREATED, summary="Crear un producto", description="Crea un nuevo producto , el campo imagen es opciona, asegúrate que sea una url")

async def create_product(model:schemas.ProductCreate, service:models_repository.ProductService=Depends(get_product_service)):

    resultado=await service.create(model)
    return resultado
    

#Ruta para obtener un producto por su id

@router.get("/get_one/{product_id}", response_model=schemas.ProductoSend, status_code=status.HTTP_200_OK)

async def get_product(product_id, service:models_repository.ProductService=Depends(get_product_service)):
        try:
            resultado=await service.get_by_id(product_id)
            return resultado
        except:
            raise HTTPException(status_code=504, detail="Limite de reintentos alcanzados")


    


#Ruta para obtener todos los productos
@router.get("/get_all",response_model=schemas.ProductsSend, status_code=status.HTTP_200_OK,description="Con este endpoint obtienes todos los productos paginados de 10 en 10, la cantidad de páginas disponibles, cantidad de productos total y tu página actual")

async def get_all_products(pagina:int=Query(default=1, gt=0,description="Introduzca la pagina que desea obtner, cada una contiene 10 resultados , si no especifica, obtendrá la página 1"),service:models_repository.ProductService=Depends(get_product_service),):
    
        resultado=await service.get_all(pagina)
        return resultado

    


#Ruta para actualizar un producto
@router.put("/update/{product_id}", response_model=schemas.ProductoSend, status_code=status.HTTP_200_OK)

async def update_product(new_product:schemas.ProductUpdate,product_id,service:models_repository.ProductService=Depends(get_product_service)):
    
    resultado=await service.update(product_id, new_product)
    return resultado

    

#Ruta para elminar un producto
@router.delete("/delete/{product_id}",  status_code=status.HTTP_200_OK)
async def delete_product(product_id:int ,service:models_repository.ProductService=Depends(get_product_service)):

    await service.delete(product_id)
    return JSONResponse(content=f"El elemento ha sido eliminado exitosamente")

#Ruta para obtener todos los productos de una categoria
@router.get("/get_by_category/{category_id}", response_model=List[schemas.ProductoSend], status_code=status.HTTP_200_OK, summary="Obten todos los productos segun su categoria")
async def get_by_category(category_id:int, service:models_repository.ProductService=Depends(get_product_service)):

    resultado=await service.get_by_category(category_id)
    return resultado

#Ruta para obtener los productos segun filtros
@router.get("/get_by_filters", response_model=List[schemas.ProductoSend], status_code=status.HTTP_200_OK)
async def filters(nombre:Optional[str]=None, precio_min:Optional[int]=None, precio_max: Optional[int]=None, category_id: Optional[int]=None, service:models_repository.ProductService=Depends(get_product_service)):

    resultado=await service.get_by_filters(nombre=nombre, precio_min=precio_min, precio_max=precio_max, category_id=category_id)
    return resultado