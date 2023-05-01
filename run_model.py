import re
from unicodedata import normalize
import os
import nltk
nltk.data.path.append(os.getcwd() + os.sep  + "nltk_data")
from nltk import corpus
from nltk import regexp_tokenize
from file_handle import file_io




class classifier_model():
  
  def __init__(self):
    self.files = object
    self.dictionary = object
    self.model_TFIDF = object
    self.index_TFIDF = object
    self.model_LSI = object
    self.index_LSI = object
    self.model_result = []
    self.model_header = []

  def set_model_parameters(self, files, dictionary, model_TFIDF, index_TFIDF, model_LSI, index_LSI):
    self.files = files
    self.dictionary = dictionary
    self.model_TFIDF = model_TFIDF
    self.index_TFIDF = index_TFIDF
    self.model_LSI = model_LSI
    self.index_LSI = index_LSI

  def set_model_result(self, model_result):
    self.model_result = model_result

  def get_model_result(self):
    return self.model_result

  def set_model_header(self, model_header):
    self.model_header = model_header

  def get_model_header(self):
    return self.model_header
  
  def start_classifier_model(self, fileType, single_multiple_class):

    
    model_result = []
    for each_file in self.files:
    
      class_data = file_io(each_file)
      #data = class_data.dispatch_filetype()

      data = class_data.switch_file_type.get(fileType, class_data.process_unknown_file_type)()
      #class_file_io.switch_single_multiple_class.get(singleMultipleClassif, class_file_io.process_unknown_classif)()      
      model_result_each_file = []
      data = normalize('NFKD', data).encode('ASCII','ignore').decode('ASCII')
      data = re.split(chr(12), data)

      for index, page in enumerate(data):
          page_number = str(index + 1)
          string_page = str(page) 
          tokenized_words = regexp_tokenize(string_page, pattern=r"\s|[ ]", gaps=True) 
          corpus_removed_stopword = corpus.stopwords.words('portuguese')
          more_stopwords = "- [ ] . , ; : | ) ( i j ' / \ l s ix t � ^ ~ - # r n" 
          corpus_removed_stopword += more_stopwords.split()
          tokenized_words_filtered = []
      
          for w in tokenized_words:
              if w not in corpus_removed_stopword:
                  tokenized_words_filtered.append(w)

          dictionary = self.dictionary
        
          class MyCorpus(object):
              def __iter__(self):
                      yield dictionary.doc2bow(tokenized_words_filtered)
                  
          corpus_memory_friendly = MyCorpus()
      
          for vector in corpus_memory_friendly:        
              if (len(vector) > 2):
                  vec_tfidf = self.model_TFIDF[vector]           
                  similarity_matriz_model_tfidf = self.index_TFIDF[vec_tfidf]                 
                  similarity_matriz_model_tfidf = sorted(enumerate(similarity_matriz_model_tfidf), key=lambda item: -item[1])
                  
                  vec_lsi = self.model_LSI[vec_tfidf]          
                  #vec_lsi = modelo_LSI[vector]
                  similarity_matriz_model_lsi = self.index_LSI[vec_lsi]  
                  similarity_matriz_model_lsi = sorted(enumerate(similarity_matriz_model_lsi), key=lambda item: -item[1])
                          
                  best_fit_tfidf_model = similarity_matriz_model_tfidf[0][1] 
                  best_fit_lsi_model = similarity_matriz_model_lsi[0][1] 
                  if (best_fit_tfidf_model > 0.60 and best_fit_lsi_model > 0.70):

                      second_best_fit_tfidf_model = similarity_matriz_model_tfidf[1][1] 
                      second_best_fit_lsi_model = similarity_matriz_model_lsi[1][1] 
                      
                      if (best_fit_tfidf_model - second_best_fit_tfidf_model) < 0.25:
                          tfidf_alert = 'alert'
                      else:
                          tfidf_alert = 'ok' 
                          
                      if (best_fit_lsi_model - second_best_fit_lsi_model) < 0.30: # a chance do primeiro melhor fit e 30% maior que a do segundo?
                          lsi_alert = 'alert'
                      else:
                          lsi_alert = 'ok'                           
                      
                      document_type = similarity_matriz_model_tfidf[0][0]
                      #classe_documento = Tipo_Documento.Documento(str(pagina), palavras_tokenize_filtradas)
                      file_name_with_extension = os.path.basename(each_file)
                      filename = os.path.splitext(file_name_with_extension)[0]
              
                      find_classification = [filename, page_number, document_type, best_fit_tfidf_model,tfidf_alert, best_fit_lsi_model, lsi_alert]                        
                      model_result_each_file.append(find_classification)
      model_result.append(model_result_each_file) 

      #data = [['16', 4, 0.832574, 'ok', 0.95689666, 'ok'], ['17', 4, 0.7490662, 'ok', 0.9434082, 'ok'], ['18', 3, 0.7548005, 'ok', 0.88454604, 'ok']]
      
      #data_dict = [dict(zip(['col1', 'col2', 'col3', 'col4', 'col5', 'col6'], row)) for row in model_result]
      #import json
      #data_json = json.dumps(data_dict)
      
      #print(data_dict)
      #print("data_json:", data_json)
      
    model_header = ['Filename','Page Number','Classification', 'Model 1 Prediction', 'Model 1 Alert', 'Model 2 Prediction', 'Model 2 Alert']
    self.set_model_result(model_result)
    self.set_model_header(model_header)
      #ee