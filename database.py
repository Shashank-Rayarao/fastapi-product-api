from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


database_url = "mysql+pymysql://root:****/fastapi_db"
engine = create_engine(database_url)
session = sessionmaker(autocommit = False, autoflush = False, bind = engine)
