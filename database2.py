from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

db_connection_string = os.environ['DB_CONNECTION_STRING']

connection_ssl_arg = {
  "ssl": {
    "ssl_ca": "/etc/ssl/cert.pem"
  }
} 



engine = create_engine(db_connection_string, connect_args = connection_ssl_arg)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# def load_jobs_from_db():
#   results_to_dict = []
  
#   with engine.connect() as connection:
#     result = connection.execute(text("select * from jobs"))
#     for row in result.all():
#       results_to_dict.append(row._asdict())
#   return results_to_dict