
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


DATABASE_URL="sqlite+aiosqlite:///./productos.db"

engine=create_async_engine(DATABASE_URL, connect_args={"check_same_thread":False})

AsyncSessionLocal=sessionmaker(autoflush=False, autocommit=False, bind=engine, class_=AsyncSession, expire_on_commit=False)

Base=declarative_base()

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

