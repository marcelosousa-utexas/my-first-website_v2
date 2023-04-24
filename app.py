import os
import nltk
from flask import Flask, render_template, jsonify
from database import load_jobs_from_db

nltk.data.path.append(os.getcwd() + os.sep  + "nltk_data")
print(nltk.data.path)
print(os.getcwd())
from nltk.corpus import stopwords

app = Flask(__name__)



print(stopwords.words('portuguese'))
print(__name__)
  
#print(sqlalchemy.__version__)  

@app.route("/")
def hello_word():
  results_to_dict = load_jobs_from_db()
  return render_template("home.html", jobs=results_to_dict)
  #return "<p> Hello, world <p>"

@app.route("/api/jobs")
def list_jobs():
  results_to_dict = load_jobs_from_db()
  return jsonify(results_to_dict)

#if __name__ == "app":
if __name__ == "__main__":  
  print("hello2")
  app.run(host = '0.0.0.0', debug = True)