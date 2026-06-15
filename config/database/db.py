from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config.env.env import env

# 1. Susun URL Koneksi
DATABASE_URL = f"{env.dbConnection}://{env.dbUser}:{env.dbPassword}@{env.dbHost}:{env.dbPort}/{env.dbName}"

# 2. Buat Engine Database
engine = create_engine(DATABASE_URL, echo=env.dbLogging)

# 3. Buat Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 4. Standar SQLAlchemy 2.0 untuk membuat Base Class Model
class Base(DeclarativeBase):
    pass


# 5. Helper Dependency Injection untuk FastAPI Controller
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
