import os
import io
#import nltk
#import pickle
from flask import Flask, render_template, request, flash, make_response, jsonify, redirect
#from database import load_jobs_from_db
from input_classificator_parameters import build_parameter
from build_classificator_model import build_model
from load_classificator_model import load_model
from user_parameters import user
import disk
from run_model import classifier_model
import csv
from werkzeug.utils import secure_filename

FILE_DIR = os.path.normpath(disk.PUBLIC_FOLDER + disk.FILE_FOLDER)

app = Flask(__name__ , static_folder=os.environ['STATIC_FOLDER'])
app.secret_key = os.environ['SECRET_KEY']
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.txt']
app.config['UPLOAD_PATH'] = FILE_DIR


class_user = user()
class_par = build_parameter()
class_save_model = build_model()
class_load_model = load_model()
class_run_model = classifier_model()
class_par.number_of_classifications = 6
class_par.number_of_parameters = 6
class_par.classification_name_list = []
class_par.parameter_name_matrix = []
classification_list, parameter_matrix, inverted_parameter_matrix = class_par.create_parameter_matrix()

@app.route("/")
def init():
  return render_template("home.html", classifications=classification_list, class_parameters=inverted_parameter_matrix)

@app.route('/upload_files', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    full_file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
    #os.path.exists(full_file_path) == False:
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid file extension", 400
        if class_user.get_type() and class_user.get_type() != file_ext:
            return "Need to keep the same extension", 400
        uploaded_file.save(full_file_path)
        #print("class_user.type: ", class_user.type)
        #if not class_user.type:
        if not class_user.get_type():
          class_user.set_type(file_ext)
        class_user.add_file(full_file_path)
    return '', 204

@app.route("/upload", methods = ['POST'])
def store_user_parameter():
  #data = request.args
  data = request.form
  print("upload_file: ", data)
  model_matrix = class_par.show_up(class_par.parameter_name_matrix, data)
  #print(model_matrix)


  lista_elementos_mais_comuns = []
  lista_elementos_mais_comuns.append(['danfe','chave','acesso','autenticidade','nf-e','www.nfe.fazenda.gov.br/portal']) #NF
  lista_elementos_mais_comuns.append(['NFS-e','verificacao','prestador','tomador','ISS','prefeitura'])  #NFm
  lista_elementos_mais_comuns.append(['autorizacao','liquidacao','pagamento','despesa','ordenador','extenso']) #autorizacao e liquidacao da despesa
  lista_elementos_mais_comuns.append(['lancamento','evento','especie','contabil','orcamentaria','decreto']) #NL
  lista_elementos_mais_comuns.append(['previsao','pagamento','pagadora','referencia','ne', 'domicilio']) #PP
  lista_elementos_mais_comuns.append(['pdet090','competencia','ordem','bancaria','bancario','domicilio']) #OB
  lista_elementos_mais_comuns.append([])


  class_par.classification_name_list = ['NF','NFm','Aut. e liq.da despesa', 'NL', 'PP', 'OB']
  
  parameter_value_matrix = lista_elementos_mais_comuns
  
  modelname = 'notas_fiscais'
  class_user.model_name = modelname

  class_save_model.build_all_models(parameter_value_matrix)
  class_save_model.save_all(modelname)

  return render_template("upload_file2.html")


@app.route('/model_result', methods=['POST'])
def test():

    
  class_load_model.load_all_models(class_user.model_name)

  dictionary = class_load_model.dictionary
  model_TFIDF = class_load_model.model_TFIDF
  index_TFIDF = class_load_model.index_TFIDF
  model_LSI =  class_load_model.model_LSI
  index_LSI = class_load_model.index_LSI

  class_run_model.set_model_parameters(class_user.get_files(), dictionary, model_TFIDF, index_TFIDF, model_LSI, index_LSI)
  class_run_model.start_classifier_model()
  model_result = class_run_model.get_model_result()
  #print(model_result)

  return render_template("model_result.html", classification=class_par.classification_name_list, model_result=model_result) 


@app.route('/get_csv', methods=['POST'])
def extract():
    # Create a CSV file from the data
    csv_data = []
    header = class_run_model.get_model_header()
    model_result = class_run_model.get_model_result()
    for file in model_result:
      for row in file:
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
  
if __name__ == "__main__":  
  app.run(host = '0.0.0.0', debug = True)