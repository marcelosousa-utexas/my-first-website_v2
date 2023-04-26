import os
from sqlalchemy import create_engine, text

db_connection_string = os.environ['DB_CONNECTION_STRING']

connection_ssl_arg = {
  "ssl": {
    "ssl_ca": "/etc/ssl/cert.pem"
  }
} 

engine = create_engine(db_connection_string, connect_args = connection_ssl_arg)



def load_jobs_from_db():
  results_to_dict = []
  
  with engine.connect() as connection:
    result = connection.execute(text("select * from jobs"))
    for row in result.all():
      results_to_dict.append(row._asdict())
  return results_to_dict