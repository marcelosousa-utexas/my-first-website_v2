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

#Save images to the 'static' folder as Flask serves images from this directory

#Create an app object using the Flask class. 
#app = Flask(__name__, static_folder="static")
#app = Flask(__name__, static_folder="public")
#app = Flask(__name__ , static_folder='/home/runner/my-first-websitev2/')

# app = Flask(__name__ , static_folder='/opt/render/project/src/public/uploads')
app = Flask(__name__ , static_folder='public')
# UPLOAD_FOLDER = 'public/uploads/'

app.secret_key = "secret key"



#Define the upload folder to save images uploaded by the user. 
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Define the upload folder to save images uploaded by the user. 

#app = Flask(__name__)

# FILES_FOLDER_ENV = 'FILES_FOLDER'
# FILES_FOLDER = os.environ[FILES_FOLDER_ENV]

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

  modelname = 'notas_fiscais'

  class_model = build_model()
  class_model.build_all_models(parameter_value_matrix)
  class_model.save_all(modelname)



  #print(data[classification_list[0]])  #return jsonify(data)
  return render_template("model_result.html")
  #return render_template("model_result.html")

  #Add Post method to the decorator to allow for form submission. 

#from config import MEDIA_FOLDER

# @app.route('/uploads/<path:filename>')
# def download_file(filename):
#     return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)


# @app.route('/files_to_classify/<path:filename>')
# def download_file(filename):
#     return send_from_directory(FILES_FOLDER, filename, as_attachment=True)

@app.route('/greet', methods=['POST'])
def submit_file():
    # print("file submitted")
    # flash('test')
    # file = request.files['file_name']
    # filename = file.filename
    # full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # flash(full_filename)
    # return render_template("model_result.html")

    # if request.method == 'GET':
    #       return render_template("model_result.html")

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
        #print(os.path.join(app.config['UPLOAD_FOLDER']))

        disk = disk_access()
        disk.write_file(file, filename)

        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], "files_to_classify/" ,filename))
        
        #file.save(os.path.join(os.environ['FILES_FOLDER'],filename))
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        #getPrediction(filename)
        label = "class1"
        print(label)
        flash(label)
        #full_filename = filename
        #full_filename = os.path.join(app.config['UPLOAD_FOLDER'], "files_to_classify/", filename)
        disk = disk_access()
        full_filename = disk.get_file_full_path(filename)
        #full_filename = os.path.join(os.environ['FILES_FOLDER'], filename)
        #full_filename = "test"
        print("full_filename: ", full_filename)
        flash(full_filename)
        file_type = "embed"
        return render_template("model_result.html", file_type=file_type)

        #           return redirect("/model_result/upload_file")
        #           #return render_template("model_result.html")
        #           #return render_template("model_result_2.html")  
        #           #return redirect('/model_result/show_file', label=label, full_filename=full_filename)
        #           #return render_template("model_result_2.html", label=label, full_filename=full_filename)

# @app.route('/model_result/upload_file', methods=['GET'])
# def show_image():
#     print("file submitted")
#     return render_template('model_result.html')


# @app.route('/model_result/show_file')
# def show_image():
#     print("show image")
#     # flash(label)
#     # flash(full_filename)
#     return render_template("model_result_2.html")
  
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