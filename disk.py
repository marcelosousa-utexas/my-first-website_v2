import os

DISK_ENV = 'DISK_FOLDER'
DISK_FOLDER = os.environ[DISK_ENV]

class disk_access():
  
  def write(self, object, filename): 
    object.save(DISK_FOLDER + filename)