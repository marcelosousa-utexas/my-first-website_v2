class build_parameter():

#  def __init__(self, int:number_of_classifications, int:number_of_parameters):
#      self.number_of_classifications = 1
#      self.number_of_parameters = 5

  def __init__(self, number_of_classifications, number_of_parameters):
    self.number_of_classifications = number_of_classifications
    self.number_of_parameters = number_of_parameters
    #self.parameter_matrix = []
    self.classification_list = []
    self.parameter_matrix = []

  def create_parameter_matrix(self):
    for i in range(0, self.number_of_classifications):
      class_text = "class_" + str(i + 1)
      #row.append("class_" + str(i + 1))
      #self.parameter_matrix["class_" + str(i + 1)] = {word}
      self.classification_list.append(class_text)
      parameters = []
      for j in range(0, self.number_of_parameters):
        parameters.append(class_text + "_parameter_" + str(j+1))
      self.parameter_matrix.append(parameters)
    # need to take the inverse of matrix to better render for HTML
    self.parameter_matrix = [[self.parameter_matrix[j][i] for j in range(len(self.parameter_matrix))] for i in range(len(self.parameter_matrix[0]))]
    return self.classification_list, self.parameter_matrix