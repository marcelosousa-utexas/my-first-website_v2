#import sqlalchemy
from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://hx90bmc7gyqxshlhb5wq:pscale_pw_FNBu1z2nXB2bhyTCMt6SeUUy1Z0LNJmpxRTh7c5gSrS@aws.connect.psdb.cloud/my-first-database?charset=utf8mb4"

connection_ssl_arg = {
  "ssl": {
    "ssl_ca": "/etc/ssl/cert.pem"
  }
} 

engine = create_engine(db_connection_string, connect_args = connection_ssl_arg)

results_to_dict = []

with engine.connect() as connection:
  result = connection.execute(text("select * from jobs"))
  #results_to_dict = []
  for row in result.all():
    results_to_dict.append(row._asdict())
  #  results_to_dict.append(dict(row))

print(results_to_dict)
  #print(result.all())

  
#print(sqlalchemy.__version__)