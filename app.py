import os
#import io
#import nltk
import pickle
from flask import Flask, render_template, jsonify, request, flash, redirect, make_response, send_from_directory, Response
from database import load_jobs_from_db
#import pandas as pd
from input_classificator_parameters import build_parameter
from build_classificator_model import build_model
from load_classificator_model import load_model
from user_parameters import user
from file_handle import file_io
from disk import disk_access
from run_model import classifier_model
#import csv
#import json
#import numpy as np

# nltk.data.path.append(os.getcwd() + os.sep  + "nltk_data")
# print(nltk.data.path)
# print(os.getcwd())
# from nltk.corpus import stopwords

app = Flask(__name__ , static_folder=os.environ['STATIC_FOLDER'])
app.secret_key = os.environ['SECRET_KEY']

class_user = user()
class_par = build_parameter(6,6)
classification_list, parameter_matrix, inverted_parameter_matrix= class_par.create_parameter_matrix()
#print(sqlalchemy.__version__)  

@app.route("/")
def init():
  return render_template("home.html", classifications=classification_list, class_parameters=inverted_parameter_matrix)

# @app.route("/api/jobs")
# def list_jobs():
#   results_to_dict = load_jobs_from_db()
#   return jsonify(results_to_dict)

@app.route("/upload_file", methods = ['POST'])
def store_user_parameter():
  #data = request.args
  data = request.form
  model_matrix = class_par.show_up(parameter_matrix, data)
  print(model_matrix)

  # parameter_value_matrix = []
  # parameter_value_matrix.append(['danfe','chave','acesso','autenticidade','nf-e','www.nfe.fazenda.gov.br/portal']) #NF
  # parameter_value_matrix.append([])

  lista_elementos_mais_comuns = []
  lista_elementos_mais_comuns.append(['danfe','chave','acesso','autenticidade','nf-e','www.nfe.fazenda.gov.br/portal']) 
  lista_elementos_mais_comuns.append(['lancamento','evento','especie','contabil','orcamentaria','decreto']) 
  lista_elementos_mais_comuns.append(['pdet090','competencia','ordem','bancaria','bancario','domicilio']) 
  lista_elementos_mais_comuns.append(['previsao','pagamento','pagadora','referencia','ne', 'domicilio']) #PP
  lista_elementos_mais_comuns.append(['autorizacao','liquidacao','pagamento','despesa','ordenador','extenso']) #autorizacao e liquidacao da despesa
  lista_elementos_mais_comuns.append(['NFS-e','verificacao','prestador','tomador','ISS','prefeitura'])  #autorizacao e liquidacao da despesa
  lista_elementos_mais_comuns.append([])

  parameter_value_matrix = lista_elementos_mais_comuns
  
  modelname = 'notas_fiscais'
  class_user.model_name = modelname

  class_model = build_model()
  #class_model.build_all_models(parameter_value_matrix)
  class_model.build_all_models(lista_elementos_mais_comuns)
  class_model.save_all(modelname)

  return render_template("upload_file.html")


@app.route('/show_file', methods=['POST'])
def submit_file():
    if request.method == 'POST':
      if 'file_name' not in request.files:
        flash('No file part')
        return redirect(request.url)
      file = request.files['file_name']
      if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
      if file:
        filename = file.filename  #Use this werkzeug method to secure filename. 
        
        class_user.file_type = "txt"
        
        disk = disk_access()
        disk.write_file(file, filename)

        label = "class1"
        print(label)
        flash(label)

        disk = disk_access()
        relative_file_path = disk.get_file_relative_path(filename)
        full_file_path = disk.get_file_absolute_path(filename)
        class_user.fullpath = full_file_path

        print("relative_file_path: ", relative_file_path)
        flash(relative_file_path)

        return render_template("confirm_file.html")

@app.route('/model_result', methods=['POST'])
def test():

  class_model = load_model()
  class_model.load_all_models(class_user.model_name)

  input_doc = class_user.fullpath
  print(input_doc)

  class_data = file_io(class_user.file_type, class_user.fullpath)
  data = class_data.dispatch_filetype()
  #print(data)

  dictionary = class_model.dictionary
  model_TFIDF = class_model.model_TFIDF
  index_TFIDF = class_model.index_TFIDF
  model_LSI =  class_model.model_LSI
  index_LSI = class_model.index_LSI

  class_model = classifier_model(data, dictionary, model_TFIDF, index_TFIDF, model_LSI, index_LSI)
  model_result = class_model.start_classifier_model()
  print(model_result)
   
  return render_template("model_result_3.html", classification=class_par.classification_name_list, data=model_result)


if __name__ == "__main__":  
  app.run(host = '0.0.0.0', debug = True)