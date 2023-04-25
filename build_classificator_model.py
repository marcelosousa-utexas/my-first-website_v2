
import warnings
from disk import disk_access
from gensim import corpora, similarities, models

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=FutureWarning, module='gensim')
#from gensim import corpora, models, similarities

class build_model():

  def __init__(self):
    self.dictionary = object 
    self.corpus = object
    self.model_TFIDF = object
    self.corpus_TFIDF = object
    self.index_TFIDF = object
    self.model_LSI = object
    self.corpus_LSI = object
    self.index_LSI = object  

  def build_all_models(self, parameter_value_list):
    self.dictionary = self.build_dict(parameter_value_list)
    self.corpus = self.build_corpus(parameter_value_list, self.dictionary)

    self.model_TFIDF = models.TfidfModel(self.corpus) #corpus_TFIDF?
    self.corpus_TFIDF = self.model_TFIDF[self.corpus]
    self.index_TFIDF = similarities.MatrixSimilarity(self.model_TFIDF[self.corpus]) #corpus_TFIDF?

    self.model_LSI = models.LsiModel(self.corpus_TFIDF, id2word=self.dictionary)
    self.corpus_LSI = self.model_LSI[self.corpus_TFIDF] #aplica o modelo para transformar o Corpus para LSI
    self.index_LSI = similarities.MatrixSimilarity(self.model_LSI[self.corpus_TFIDF])
    

  def save_all(self, modelname):
    self.write_to_disk(self.dictionary, modelname, ".dict")
    
    self.write_to_disk(self.model_TFIDF, modelname, ".tfidf")
    self.write_to_disk(self.index_TFIDF, modelname, "_tfidf.index")

    self.write_to_disk(self.model_LSI, modelname, ".lsi")
    self.write_to_disk(self.index_LSI, modelname, "_lsi.index")
    



  
  def build_dict(self, parameter_value_list):
    dictionary = corpora.Dictionary(parameter_value_list)
    return dictionary

  def build_corpus(self, parameter_value_list, dictionary):
    corpus = [dictionary.doc2bow(text) for text in parameter_value_list]
    return corpus

  # def build_tfidf(self, corpus):
  #   tfidf_model = models.TfidfModel(corpus) 
  #   return tfidf_model
  
  def write_to_disk(self, object, modelname, type):
    filename = modelname + type
    disk = disk_access()
    disk.write(object, filename)

  # def save_all(self, parameter_value_list, modelname):
  #   self.write_to_disk(self, object, modelname, type)
  #   filename = modelname + type
  #   disk = disk_access()
  #   disk.write(object, filename)
    
  #   dictionary = self.build_dict(parameter_value_list)
  #   corpus = self.build_corpus(parameter_value_list, dictionary)
  #   corpus_TFIDF = self.build_tfidf(corpus)
  #   corpus_LSI = self.build_tfidf(corpus_TFIDF) #corpus?
  #   model_TFIDF = models.TfidfModel(corpus) #corpus_TFIDF?
  #   model_LSI = models.LsiModel(corpus_TFIDF, id2word=dictionary) #corpus_LSI?
  #   index_TFIDF = similarities.MatrixSimilarity(model_TFIDF[corpus]) #corpus_TFIDF?
  #   index_LSI = similarities.MatrixSimilarity(model_LSI[corpus_TFIDF])


  # def build_dict(self, parameter_value_list, modelname):
  #   type = '.dict'
  #   #modelname = 'dicionario_palavras_chave'
  #   dictionary = corpora.Dictionary(parameter_value_list)
  #   self.write_to_disk(dictionary, modelname, type)
  #   #print(os.environ['DISK_FOLDER'] + 'dicionario_palavras_chave.dict')
  #   #dictionary.save('/var/data/models/dicionario_palavras_chave.dict')


  


  # def dispatch_model(self, document_type):
  #     """Dispatch method"""
  #     method = getattr(self, document_type, lambda: "Model is not available")
  #     # Call the method as we return it
  #     return method()



  
  # def build_dict(self, parameter_value_list, modelname):
  #   type = '.dict'
  #   #modelname = 'dicionario_palavras_chave'
  #   dictionary = corpora.Dictionary(parameter_value_list)
  #   self.write_to_disk(dictionary, modelname, type)
  #   #print(os.environ['DISK_FOLDER'] + 'dicionario_palavras_chave.dict')
  #   #dictionary.save('/var/data/models/dicionario_palavras_chave.dict')

# corpora.MmCorpus.serialize('C:/TesteOCR/Python/matriz_corpus_dicionario_palavras_chave_original.mm', corpus)  # store to disk, for later use
# #pprint(corpus)


