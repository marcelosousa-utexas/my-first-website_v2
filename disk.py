import os

MODELS_FOLDER_ENV = 'MODELS_FOLDER'
MODELS_FOLDER = os.environ[MODELS_FOLDER_ENV]

FILES_FOLDER_ENV = 'FILES_FOLDER'
FILES_FOLDER = os.environ[FILES_FOLDER_ENV]

class disk_access():
 
  def write_model(self, object, filename): 
    object.save(MODELS_FOLDER + filename)

  def write_file(self, object, filename): 
    #object.save(FILES_FOLDER + filename)
    object.save(os.path.join(FILES_FOLDER,filename))
  

  def get_file_full_path(self, filename): 
    return (FILES_FOLDER + filename)