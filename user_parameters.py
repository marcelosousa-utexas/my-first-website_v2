
class user():

  def __init__(self):
    self.model_name = ""
    self.file_type = ""
    self.files = []
    self.type = ""

  def add_file(self, fullpath):
    self.files.append(fullpath)

  def get_files(self):
    return self.files

  def set_type(self, type):
    self.type = type

  def get_type(self):
    return self.type