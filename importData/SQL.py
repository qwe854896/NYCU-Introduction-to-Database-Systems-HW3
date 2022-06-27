import sqlalchemy
from sqlalchemy.orm import (
	declarative_base,
	sessionmaker
)
from sqlalchemy import Table, Column, Integer, Text, Numeric


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


def fetchConn():
	con = connect(username, password, db_name, rds_host, db_port)
	return con