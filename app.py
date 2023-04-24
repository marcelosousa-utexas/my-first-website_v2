import os
import nltk
from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db
from input_classificator_parameters import build_parameter
from build_classificator_model import build_model

# nltk.data.path.append(os.getcwd() + os.sep  + "nltk_data")
# print(nltk.data.path)
# print(os.getcwd())
# from nltk.corpus import stopwords

app = Flask(__name__)

# print(stopwords.words('portuguese'))
# print(__name__)

class_par = build_parameter(1,6)
classification_list, parameter_matrix, inverted_parameter_matrix= class_par.create_parameter_matrix()
#print(sqlalchemy.__version__)  

@app.route("/")
def hello_word():
  #n_classifications, n_parameters
  return render_template("home.html", classifications=classification_list, class_parameters=inverted_parameter_matrix)
  #return "<p> Hello, world <p>"

@app.route("/api/jobs")
def list_jobs():
  results_to_dict = load_jobs_from_db()
  return jsonify(results_to_dict)

@app.route("/model_result", methods = ['POST'])
def store_user_parameter():
  #data = request.args
  data = request.form
  model_matrix = class_par.show_up(parameter_matrix, data)
  print(model_matrix)

  parameter_value_matrix = []
  parameter_value_matrix.append(['danfe','chave','acesso','autenticidade','nf-e','www.nfe.fazenda.gov.br/portal']) #NF
  parameter_value_matrix.append([])

  class_model = build_model()
  class_model.write_dict(parameter_value_matrix)
  
  #print(data[classification_list[0]])
  return jsonify(data)
  #return render_template("model_result.html")

# @app.route("/model_result", methods=['POST'])
# @app.route("/model_result", methods=['GET', 'POST'])
# def model_result():
#     if request.method == 'POST':
#         #data = request.method 
#         #print(data)
#         return render_template('model_result.html', class_1 = request.form['class_1'])
      
#     elif request.method == 'GET':
#         print('A GET request was made')
#         #return render_template('model_result.html', model_result=request.form['model_result'])

#     else:
#         return 'Not a valid request method for this route'

#if __name__ == "app":
if __name__ == "__main__":  
  print("hello2")
  app.run(host = '0.0.0.0', debug = True)