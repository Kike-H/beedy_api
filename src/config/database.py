from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os 

load_dotenv()
meta = MetaData()

USER = os.environ.get('USERDB')
PASSWORD = os.environ.get('PASSWORDDB')
DATABASE = os.environ.get('DATABASE')

engine = create_engine("mysql+pymysql://%s:%s@localhost:3306/%s"%(USER, PASSWORD, DATABASE))
conn = engine.connect()