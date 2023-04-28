import os
import io
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
import csv
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


class_save_model = build_model()
class_load_model = load_model()
class_run_model = classifier_model()
classification_list, parameter_matrix, inverted_parameter_matrix= class_par.create_parameter_matrix()
#print(sqlalchemy.__version__)  

@app.route("/")
def init():
  return render_template("home2.html", classifications=classification_list, class_parameters=inverted_parameter_matrix)

# @app.route("/api/jobs")
# def list_jobs():
#   results_to_dict = load_jobs_from_db()
#   return jsonify(results_to_dict)

@app.route("/upload_file", methods = ['POST'])
def store_user_parameter():
  #data = request.args
  data = request.form
  print("upload_file: ", data)
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


  
  #class_model.build_all_models(parameter_value_matrix)
  class_save_model.build_all_models(lista_elementos_mais_comuns)
  class_save_model.save_all(modelname)

  return render_template("upload_file2.html")


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

        return render_template("confirm_file2.html")

@app.route('/model_result', methods=['POST'])
def test():


  class_load_model.load_all_models(class_user.model_name)

  input_doc = class_user.fullpath
  print(input_doc)

  class_data = file_io(class_user.file_type, class_user.fullpath)
  data = class_data.dispatch_filetype()
  #print(data)

  dictionary = class_load_model.dictionary
  model_TFIDF = class_load_model.model_TFIDF
  index_TFIDF = class_load_model.index_TFIDF
  model_LSI =  class_load_model.model_LSI
  index_LSI = class_load_model.index_LSI

  class_run_model.set_model_parameters(data, dictionary, model_TFIDF, index_TFIDF, model_LSI, index_LSI)
  class_run_model.start_classifier_model()
  model_result = class_run_model.get_model_result()

  #print(model_result)
  #classification = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6']

  return render_template("bootstrap_table.html", classification=class_par.classification_name_list, data=model_result) 
  #print(model_result)
  #data = [{'name': 'John', 'age': 30, 'city': 'New York'},{'name': 'Lucas', 'age': 20, 'city': 'Austin'}]
  #return render_template("table.html", parameters=data) 
  #return render_template("model_result_8.html", classifications=class_par.classification_name_list, class_parameters=model_result)
  


# @app.route('/get_csv', methods=['POST'])
# def extract():
#     data = request.form
#     print("data request:", data)
#     # import json
#     # data_json = json.dumps(data)
#     # print(data_json)
#     # print(type(data_json))
#     return jsonify(data)

@app.route('/get_csv', methods=['POST'])
def extract():
    # Create a CSV file from the data
    csv_data = []
    header = class_run_model.get_model_header()
    data = class_run_model.get_model_result()
    for row in data:
      data_row = []
      for cell in row:
        data_row.append(cell)
      csv_data.append(data_row)
    csv_file = io.StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(header)
    writer.writerows(csv_data)
    
    # Create a response object with the CSV file
    response = make_response(csv_file.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

@app.route('/extract', methods=['POST'])
def extract_table():
    data = request.form
    print("data request:", data)
    return data

    # response = Response(x.getvalue(), mimetype='text/csv')
    # response.headers.set("Content-Disposition", "attachment", filename="my_data.csv")
    # response.headers.set("Cache-Control", "no-cache")
    # return response
    # Get dataframe from request data
    # df = pd.read_json(request.data, orient='split')

    # # Convert dataframe to CSV in memory
    # csv_output = io.BytesIO()
    # df.to_csv(csv_output, index=False, encoding='utf-8')

    # # Return CSV as Flask response with headers
    # response = Response(csv_output.getvalue(), mimetype='text/csv')
    # response.headers.set("Content-Disposition", "attachment", filename="my_data.csv")
    # response.headers.set("Cache-Control", "no-cache")
    # return response
  
if __name__ == "__main__":  
  app.run(host = '0.0.0.0', debug = True)