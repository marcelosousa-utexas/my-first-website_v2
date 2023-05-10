class build_parameter():
  
  def __init__(self):
    self.number_of_classifications = 6
    self.number_of_parameters = 6
    self.classification_name_list = []
    self.parameter_name_matrix = []
    self.inverted_parameter_name_matrix = []
    self.data_matrix = []
    self.header = []    

  def set_number_of_classifications(self, number_of_classifications):
    self.number_of_classifications = number_of_classifications

  def get_number_of_classifications(self):
    return self.number_of_classifications
  
  def set_number_of_parameters(self, number_of_parameters):
    self.number_of_parameters = number_of_parameters

  def get_number_of_parameters(self):
    return self.number_of_parameters
  
  def set_data_matrix(self, data_matrix):
    self.data_matrix = data_matrix

  def get_data_matrix(self):
    return self.data_matrix

  def set_header(self, header):
    self.header = header

  def get_header(self):
    return self.header
  
  def create_parameter_matrix(self):
    for i in range(0, self.number_of_classifications):
      class_text = "class_" + str(i + 1)
      self.classification_name_list.append(class_text)
      parameters = []
      for j in range(0, self.number_of_parameters):
        parameters.append(class_text + "_parameter_" + str(j+1))
      self.parameter_name_matrix.append(parameters)
    self.inverted_parameter_name_matrix = self.invert_matrix(self.parameter_name_matrix)
    # need to take the inverse of matrix to better render for HTML
    return self.classification_name_list, self.parameter_name_matrix, self.inverted_parameter_name_matrix

  def invert_matrix(self, parameter_name_matrix):
    return [[parameter_name_matrix[j][i] for j in range(len(parameter_name_matrix))] for i in range(len(parameter_name_matrix[0]))]
    
  
  def build_data_matrix(self, parameter_name_matrix, data):
    parameter_value_matrix = []
    for list_name_parameters in parameter_name_matrix:
      parameter_value_list = []
      for each_parameter in list_name_parameters:
        parameter_value_list.append(data[each_parameter])
      parameter_value_matrix.append(parameter_value_list)
    # parameter_value_matrix.append([])
    return parameter_value_matrix

  def build_header(self, classification_name_list, data):
    classification_value_list = []
    for list_name_classification in classification_name_list:
      classification_value_list.append(data[list_name_classification])
    # parameter_value_matrix.append([])
    return classification_value_list