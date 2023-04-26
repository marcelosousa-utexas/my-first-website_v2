import os

MODELS_FOLDER_ENV = 'MODELS_FOLDER'
MODELS_FOLDER = os.environ[MODELS_FOLDER_ENV]

FILES_FOLDER_ENV = 'FILES_FOLDER'
FILES_FOLDER = os.environ[FILES_FOLDER_ENV]

FILES_LOAD_ENV = 'FILE_LOAD'
FILES_LOAD = os.environ[FILES_LOAD_ENV]

class disk_access():
 
  def write_model(self, object, filename): 
    object.save(MODELS_FOLDER + filename)

  def write_file(self, object, filename): 
    #object.save(FILES_FOLDER + filename)
    object.save(os.path.join(FILES_FOLDER,filename))
  

  def get_file_full_path(self, filename): 
    print("I'm here")
    print(os.path.join(os.path.dirname(FILES_LOAD), filename))
    print(FILES_LOAD + filename)
    print(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'filename'))
    
    return os.path.join(os.path.dirname(FILES_LOAD), filename)
    #return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'filename')