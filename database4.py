import os
from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from models import Jobs

class Database():
    # replace the user, password, hostname and database according to your configuration according to your information
    db_connection_string = os.environ['DB_CONNECTION_STRING']
    
    connection_ssl_arg = {
      "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
      }
    } 
        
  
    engine = db.create_engine(db_connection_string, connect_args = connection_ssl_arg)
    def __init__(self):
        self.connection = self.engine.connect()
        print("DB Instance created")

    def fetchAllUsers(self):
        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)        
        customers = self.session.query(Jobs).all()
        for cust in customers:
            print(cust)
