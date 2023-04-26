import os
#import nltk
import pickle
from flask import Flask, render_template, jsonify, request, flash, redirect, send_from_directory
from database import load_jobs_from_db
from input_classificator_parameters import build_parameter
from build_classificator_model import build_model
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
def hello_word():
  return render_template("home.html", classifications=classification_list, class_parameters=inverted_parameter_matrix)

# @app.route("/api/jobs")
# def list_jobs():
#   results_to_dict = load_jobs_from_db()
#   return jsonify(results_to_dict)

@app.route("/model_result", methods = ['POST'])
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

  return render_template("model_result.html")


@app.route('/greet', methods=['POST'])
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
        return render_template("model_result_3.html", file_type=file_type)

@app.route('/test', methods=['POST'])
def test():
  return render_template("model_result_4.html")

if __name__ == "__main__":  
  app.run(host = '0.0.0.0', debug = True)