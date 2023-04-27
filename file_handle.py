class file_io():

  def __init__(self, file_type, file_full_path):
    self.file_type = file_type
    self.file_full_path = file_full_path
  
  def dispatch_filetype(self):
      """Dispatch method"""
      method_name = 'read_' + self.file_type
      # Get the method from 'self'. Default to a lambda.
      method = getattr(self, method_name, lambda: "Wrong document type")
      # Call the method as we return it
      return method()
  
  def read_txt(self):
    with open(self.file_full_path, encoding="utf8") as txt_file:
      data = txt_file.read().lower()
    return data
  
  def read_pdf(self):
      return None



  