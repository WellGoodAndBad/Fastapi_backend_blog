import databases, sqlalchemy, os
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


user = os.environ.get('DB_USER',  'postgres')
password = os.environ.get('DB_PASSWORD',  'postgres')
db_addr = 'localhost'
db_name = 'test_db'

DATABASE_URL = f"postgresql://{user}:{password}@{db_addr}/{db_name}"

database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
