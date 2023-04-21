#import sqlalchemy
from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://amiezd22ops2rw1jjl1u:pscale_pw_Nb71unYyVg7zLteFUDRlOiLVzfYTTWr0iDugqbOgOyv@aws.connect.psdb.cloud/my-first-database?charset=utf8mb4"

connect_ssl_arg = {
  "ssl": {
    "ssl_ca": "/etc/ssl/cert.pem"
  }
} 

engine = create_engine(db_connection_string, connect_args = connect_ssl_arg)


with engine.connect() as connection:
    result = connection.execute(text("select * from jobs"))
#    for row in result:
#        print("title:", #row["location"])

print(result.all())


  
#print(sqlalchemy.__version__)