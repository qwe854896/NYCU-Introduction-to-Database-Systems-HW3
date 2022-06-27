import sqlalchemy
from sqlalchemy.orm import (
	declarative_base,
	sessionmaker
)
from sqlalchemy import Table, Column, Integer, Text, Numeric


# Log
import os
import logging

logger = logging.getLogger('')
if   os.environ['Log_level'] == 'DEBUG':
    logger.setLevel(logging.DEBUG)
elif os.environ['Log_level'] == 'INFO':
    logger.setLevel(logging.INFO)


# rds settings
import rds_config
rds_host  = rds_config.rds_host
username  = rds_config.db_username
password  = rds_config.db_password
db_name   = rds_config.db_name
db_port   = rds_config.db_port


# def connect(user=username, password=password, db=db_name, host=rds_host, port=db_port):
def connect(user, password, db, host='localhost', port=5432):
	'''Returns a connection and a metadata object'''
	url = 'postgresql://{}:{}@{}:{}/{}'
	url = url.format(user, password, host, port, db)

	con = sqlalchemy.create_engine(url, client_encoding='utf8')
	return con


Base = declarative_base()
con = connect(username, password, db_name, rds_host, db_port)

class Video_Games(Base):
	__table__ = Table('video_games', Base.metadata, autoload=True, autoload_with=con)
    
    # __tablename__ = 'video_games'
    # Name =            Column(Text, primary_key=True)
    # Platform =        Column(Text, primary_key=True)
    # Year_of_Release = Column(Integer, primary_key=True)
    # Genre =           Column(Text)
    # Publisher =       Column(Text)
    # NA_Sales =        Column(Numeric(7, 3))
    # EU_Sales =        Column(Numeric(7, 3))
    # JP_Sales =        Column(Numeric(7, 3))
    # Other_Sales =     Column(Numeric(7, 3))
    # Global_Sales =    Column(Numeric(7, 3))
    # Critic_Score =    Column(Integer)
    # Critic_Count =    Column(Integer)
    # User_Score =      Column(Numeric(7, 3))
    # User_Count =      Column(Integer)
    # Developer =       Column(Text)
    # Rating =          Column(Text)


Session = sessionmaker(bind=con)

def fetchSession():
    return Session()