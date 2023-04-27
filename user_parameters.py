
class user():

  def __init__(self):
    self.model_name = ""
    self.file_type = ""
    self.fullpath = ""
    self.type = ""
    self.file = object

  def set_file(self, object):
    self.file = object

  def get_file(self):
    return self.file