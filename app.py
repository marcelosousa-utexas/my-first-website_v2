import os
#import nltk
import pickle
from flask import Flask, render_template, jsonify, request, flash, redirect, send_from_directory
from database import load_jobs_from_db
from input_classificator_parameters import build_parameter
from build_classificator_model import build_model
from load_classificator_model import load_model
from disk import disk_access

# nltk.data.path.append(os.getcwd() + os.sep  + "nltk_data")
# print(nltk.data.path)
# print(os.getcwd())
# from nltk.corpus import stopwords

app = Flask(__name__ , static_folder=os.environ['STATIC_FOLDER'])
app.secret_key = os.environ['SECRET_KEY']

class_par = build_parameter(1,6)
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

  parameter_value_matrix = []
  parameter_value_matrix.append(['danfe','chave','acesso','autenticidade','nf-e','www.nfe.fazenda.gov.br/portal']) #NF
  parameter_value_matrix.append([])

  modelname = 'notas_fiscais'

  class_model = build_model()
  class_model.build_all_models(parameter_value_matrix)
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

        disk = disk_access()
        disk.write_file(file, filename)

        label = "class1"
        print(label)
        flash(label)

        disk = disk_access()
        full_filename = disk.get_file_relative_path(filename)

        print("full_filename: ", full_filename)
        flash(full_filename)
        file_type = "embed"
        return render_template("confirm_file.html", file_type=file_type)

@app.route('/model_result', methods=['POST'])
def test():

  modelname = 'notas_fiscais'
  class_model = load_model()
  class_model.load_all_models(modelname)

  dictionary = class_model.dictionary
  model_TFIDF = class_model.model_TFIDF
  index_TFIDF = class_model.index_TFIDF
  model_LSI =  class_model.model_LSI
  index_LSI = class_model.index_LSI


  # modelo_TFIDF = models.TfidfModel.load('C:/TesteOCR/Python/modelo_TFIDF.tfidf')
  # modelo_LSI = models.LsiModel.load('C:/TesteOCR/Python/modelo_LSI.lsi')
            
  # index_TFIDF = similarities.MatrixSimilarity.load('C:/TesteOCR/Python/matriz_similaridade_TFIDF.index')
  # index_LSI = similarities.MatrixSimilarity.load('C:/TesteOCR/Python/matriz_similaridade_LSI.index')
  
  return render_template("model_result.html")

if __name__ == "__main__":  
  app.run(host = '0.0.0.0', debug = True)