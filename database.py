#import sqlalchemy
from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://0b9zcnwnos296ynimcb1:pscale_pw_WGDIbhpuHN5CS3uGudG7p4yKQZd9k5LEsmR1X8cbGpN@aws.connect.psdb.cloud/my-first-database?charset=utf8mb4"

connection_ssl_arg = {
  "ssl": {
    "ca": "/etc/ssl/cert.pem"
  }
} 

engine = create_engine(db_connection_string, connect_args = connection_ssl_arg)


with engine.connect() as connection:
    result = connection.execute(text("select * from jobs"))
#    for row in result:
#        print("title:", #row["location"])

print(result.all())


  
#print(sqlalchemy.__version__)