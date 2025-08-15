from fastapi import APIRouter, Depends, status
from fastapi.responses import  JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import database, models, schemas
from repositorys import models_repository
from typing import List


#Funcion para obtener la session como dependencia
def get_db(db:AsyncSession=Depends(database.get_session)):
    return  db

#Funcion para obtener ProductService como dependencia

def get_product_service(session:AsyncSession=Depends(get_db)):
    return models_repository.CategoryRepository(session,models.Category )

router=APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/create", response_model=schemas.CategorySend, status_code=status.HTTP_201_CREATED)
async def create_category(model:schemas.CategoryCreate,service:models_repository.CategoryRepository=Depends(get_product_service)):
    category=await service.create(model)
    return category

@router.get("/get_by_id/{category_id}", response_model=schemas.CategorySend, status_code=status.HTTP_200_OK)
async def get_category(category_id: int,service:models_repository.CategoryRepository=Depends(get_product_service)):
    category=await service.get_by_id(category_id)
    return category

@router.get("/get_all", response_model=List[schemas.CategorySend], status_code=status.HTTP_200_OK)
async def get_all_categorys(service:models_repository.CategoryRepository=Depends(get_product_service)):
    categorys=await service.get_all()
    return categorys


@router.delete("/delete/{category_id}",  status_code=status.HTTP_200_OK)
async def delete_category(category_id: int,service:models_repository.CategoryRepository=Depends(get_product_service)):
    category=await service.delete(category_id)
    return JSONResponse(content={"message":f"Se ha eliminado correctamente el objeto{category.__name__}"})
    
@router.put("/update/{category_id}",  status_code=status.HTTP_200_OK)
async def update_category(category_id:int,model:schemas.CategoryUpdate, service:models_repository.CategoryRepository=Depends(get_product_service)):
    category=await service.update(category_id,model)
    return JSONResponse(content={"message":f"Se ha actualizado correctamente el objeto{category.__name__}"})
    