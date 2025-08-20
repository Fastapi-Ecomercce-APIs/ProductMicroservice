import asyncio
from fastapi import  Request,HTTPException


from main import app

#Middleware para timeout
@app.middleware("http")
async def timeout(request:Request, call_next):
    try:
        return await asyncio.wait_for(call_next(request), timeout=20)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="El tiempo de espera se ha agotado")
    


