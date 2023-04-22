from flask import Flask, render_template

from database import load_jobs_from_db
#from sqlalchemy import text

app = Flask(__name__)


  
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