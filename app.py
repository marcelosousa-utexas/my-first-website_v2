import os
import io
#import nltk
#import pickle
from flask import Flask, render_template, request, flash, make_response, jsonify, redirect, url_for
#from database import load_jobs_from_db
from input_classificator_parameters import build_parameter
from build_classificator_model import build_model
from load_classificator_model import load_model
from user_parameters import user
import disk
from run_model import classifier_model
import csv
from werkzeug.utils import secure_filename
from file_handle import file_io

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
class_file_io = file_io("")

from database3 import Database
#from models import Base
#from database3 import SessionLocal, engine

class_db = Database()
#engine = class_db.engine


@app.route("/")
def init():
  return render_template("home.html")

@app.route('/new_load_model', methods=['POST'])
def new_load_model():
  if request.form:
      option = request.form.getlist('inlineRadioOptions')
      if len(option) > 0:
        if option[0].__contains__('new_model'):
          print('new_model')
          class_user.set_new_model(True)
          return render_template('new_model_n_parameters.html')
        elif option[0].__contains__('load_model'):
          print('load_model')
          class_user.set_new_model(False)
          models = class_db.fetchAllModels()
          print(models)
          return render_template("load_models.html", models=models) 
        else:
          return "Invalid option", 400
    

# @app.route('/new_load_model', methods=['GET','POST'])
# def new_load_model():
#   if request.method == 'POST':
#     if request.form:
#         option = request.form.getlist('inlineRadioOptions')
#         if len(option) > 0:
#           if option[0].__contains__('new_model'):
#             print('new_model')
#             class_user.set_new_model(True)
#             return render_template('new_model_n_parameters2.html')
#           elif option[0].__contains__('load_model'):
#             print('load_model')
#             class_user.set_new_model(False)
#             return render_template("load_model_n_parameters.html") 
#           else:
#             return "Invalid option", 400
#   else:
#     class_user.set_new_model(True)
#     return render_template('new_model_n_parameters2.html')    
    
# @app.route("/model_name_validation")
# def model_name_validation():
#   print("model validation")
#   #return render_template('new_model_n_parameters2.html')
#   return redirect(url_for('new_load_model'))
#   #return redirect('/new_load_model')

@app.route('/check_input', methods=['POST'])
def check_input():
  modelName = request.form['modelName']
  print(modelName)
  exists = class_db.search(modelName)
  print(exists)
  response = {'exists': exists}
  resp = jsonify(response)
  print(resp)
  return resp

# @app.route("/api/jobs")
# def list_jobs():
#   results_to_dict = load_jobs_from_db()
#   return jsonify(results_to_dict)

@app.route("/n_parameters", methods=['POST'])
def n_parameters():
    if request.form:
      flash("That username is already taken...")
      #numClass = 6

      modelName = request.form['modelName']
      class_user.model_name = modelName
      
      numClass = request.form['numClass']
      print(numClass)
      numParams = request.form['numParams']
      #numParams = 1
      class_par.set_number_of_classifications(int(numClass))
      class_par.set_number_of_parameters(int(numParams))
      class_par.classification_name_list = []
      class_par.parameter_name_matrix = []
      classification_list, parameter_matrix, inverted_parameter_matrix = class_par.create_parameter_matrix()
      #response = {'data': numClass}
      #return jsonify(response)
      # Do something with the numParams and numClass values
      return render_template("new_model_define_parameters.html", classifications=classification_list, numParams = class_par.get_number_of_parameters(), class_parameters=inverted_parameter_matrix)


@app.route("/store_user_parameter", methods = ['POST'])
def store_user_parameter():
  if request.form:
    #data = request.args
    data = request.form
    print("parameter_data : ", data)
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

    lista_elementos_mais_comuns = []
    lista_elementos_mais_comuns.append(['edital','licitacao','supensao','concurso']) #SEACOMP
    lista_elementos_mais_comuns.append(['pessoal','aposentadoria','beneficio','salario'])  #SEFIPE
    lista_elementos_mais_comuns.append(['auditoria','fiscalizacao','regularidade','lei']) #SEAUD
    lista_elementos_mais_comuns.append(['contas','governo','gestao','fiscal']) #SEMAG
    lista_elementos_mais_comuns.append(['contas','tomada','prestacao','regular']) #SECONT
    lista_elementos_mais_comuns.append([])
    
  
    class_par.classification_name_list = ['NF','NFm','Aut. e liq.da despesa', 'NL', 'PP', 'OB']
    class_par.classification_name_list = ['SEACOMP','SEFIPE', 'SEAUD', 'SEMAG', 'SECONT']
    
    parameter_value_matrix = lista_elementos_mais_comuns
    
    #modelname = 'notas_fiscais'
    #class_user.model_name = modelname
  
    class_save_model.build_all_models(parameter_value_matrix)
    class_save_model.save_all(class_user.model_name)
  
    return render_template("upload_file_type.html")        
    #return render_template("upload_file.html")


@app.route('/upload', methods=['POST'])
def upload():
    if request.form:
      fileType = request.form.get('file_type')
      singleMultipleClassif = request.form.get('single_multiple_class')
      if fileType == 'plain_text':
        return render_template("text_message_box.html")
      
      else:
          
        print(fileType)
        print(singleMultipleClassif)

        class_file_io.set_file_type(fileType)
        class_file_io.set_single_multiple_class(singleMultipleClassif)
  
  
        #class_file_io.switch_file_type.get(fileType, class_file_io.process_unknown_file_type)()
        #class_file_io.switch_single_multiple_class.get(singleMultipleClassif, class_file_io.process_unknown_classif)()
    
  
        return render_template("upload_file.html")
    
  
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

@app.route('/upload_plain_text', methods=['POST'])
def upload_plain_text():
    # Get the text from the textarea input
    if request.form:
      text = request.form['scroll-box']
      filename = 'plain_text.txt'
      file_ext = os.path.splitext(filename)[1]
      full_file_path = os.path.join(app.config['UPLOAD_PATH'], filename)

      # Write the text to a file on the server
      with open(full_file_path, 'w') as file:
          file.write(text)
      class_user.set_type(file_ext)
      class_user.add_file(full_file_path)
      
      # Return a response to the client
      return redirect(url_for('model_result'))

@app.route('/model_result', methods=['GET','POST'])
def model_result():

    
  class_load_model.load_all_models(class_user.model_name)

  dictionary = class_load_model.dictionary
  model_TFIDF = class_load_model.model_TFIDF
  index_TFIDF = class_load_model.index_TFIDF
  model_LSI =  class_load_model.model_LSI
  index_LSI = class_load_model.index_LSI

  class_run_model.set_model_parameters(class_user.get_files(), dictionary, model_TFIDF, index_TFIDF, model_LSI, index_LSI)
  class_run_model.start_classifier_model(class_file_io.get_file_type(), class_file_io.get_single_multiple_class())
  model_result = class_run_model.get_model_result()

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