from fastapi import FastAPI
from routes import category_routes, products_routes
import database

app=FastAPI()

app.include_router(category_routes.router)
app.include_router(products_routes.router)


@app.on_event("startup")
async def startup_event():
    print("Conectando...")
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)