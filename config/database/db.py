# 1. FIXED: Hapus 'create_all' karena tidak ada di dalam sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.env.env import env

# 2. Susun URL Koneksi
DATABASE_URL = f"{env.dbConnection}://{env.dbUser}:{env.dbPassword}@{env.dbHost}:{env.dbPort}/{env.dbName}"

# 3. Buat Engine Database
engine = create_engine(DATABASE_URL, echo=env.dbLogging)

# 4. Buat Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Buat Base Class untuk Model-Model ORM (UserModel, RoleModel, dll.)
Base = declarative_base()


# 6. Helper Dependency Injection untuk FastAPI Controller
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
