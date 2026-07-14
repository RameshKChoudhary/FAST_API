from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://neondb_owner:npg_6bIRx5Jgwryd@ep-delicate-dawn-ad9x94q3-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal =sessionmaker(autocommit=False,autoflush=False,bind= engine)

Base = declarative_base()

 

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()