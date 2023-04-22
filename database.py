#import sqlalchemy
from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://rcwucdd88v6gqzvyfixy:pscale_pw_V82cL2rNV5PMZ8acg2imrqmdJ8ZPjJLcilscXdudF8d@aws.connect.psdb.cloud/my-first-database?charset=utf8mb4"

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
    #results_to_dict = []
    for row in result.all():

      

      results_to_dict.append(row._asdict())
    #  results_to_dict.append(dict(row))
  return results_to_dict
  #print(results_to_dict)
    #print(result.all())
