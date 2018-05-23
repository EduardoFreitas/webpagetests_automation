from sqlalchemy import create_engine
from settings import load_configuration
from sqlalchemy.orm import sessionmaker
import os

load_configuration()

db_username = os.environ["db_username"]
db_password = os.environ["db_password"]
db_name = os.environ["db_name"]
host = os.environ["host"]

conn_data = 'mysql+pymysql://{}:{}@{}/{}'.format(db_username, db_password, host, db_name)
engine = create_engine(conn_data, echo=True)
Session = sessionmaker(bind=engine)


