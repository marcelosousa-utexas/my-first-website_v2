import os

MODELS_FOLDER_ENV = 'MODELS_FOLDER'
MODELS_FOLDER = os.environ[MODELS_FOLDER_ENV]

PUBLIC_FOLDER_ENV = 'PUBLIC_FOLDER'
PUBLIC_FOLDER = os.environ[PUBLIC_FOLDER_ENV]

FILE_FOLDER_ENV = 'FILE_FOLDER'
FILE_FOLDER = os.environ[FILE_FOLDER_ENV]

STATIC_FOLDER_ENV = 'STATIC_FOLDER'
STATIC_FOLDER = os.environ[STATIC_FOLDER_ENV]

class disk_access():
 
  def write_model(self, object, filename): 
    path = PUBLIC_FOLDER + MODELS_FOLDER + filename
    path = os.path.normpath(path)
    object.save(path)

  def write_file(self, object, filename): 
    path = PUBLIC_FOLDER + FILE_FOLDER + filename
    path = os.path.normpath(path)
    object.save(path)
  

  def get_file_relative_path(self, filename): 
    path = os.sep + STATIC_FOLDER + FILE_FOLDER + filename
    path = os.path.normpath(path)    
    return path

  def get_model_absolute_path(self, filename): 
    path = os.sep + PUBLIC_FOLDER + MODELS_FOLDER + filename
    path = os.path.normpath(path)    
    return path    

  def get_file_absolute_path(self, filename): 
    path = os.sep + PUBLIC_FOLDER + FILE_FOLDER + filename
    path = os.path.normpath(path)    
    return path       

  # def loadfile(self, object, filename): 
  #   path = self.get_file_relative_path(filename)
  #   return object.load(path)