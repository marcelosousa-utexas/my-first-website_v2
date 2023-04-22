from flask import Flask, render_template

from database import engine
from sqlalchemy import text

app = Flask(__name__)




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

  
#print(sqlalchemy.__version__)  

@app.route("/")
def hello_word():
  results_to_dict = load_jobs_from_db()
  return render_template("home.html", jobs=results_to_dict)
  #return "<p> Hello, world <p>"

#if __name__ == "__name__":  
if __name__ == "app":
  print("hello2")
  app.run(host = '0.0.0.0', debug = True)