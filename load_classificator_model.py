
import warnings
from disk import disk_access
from gensim import corpora, similarities, models

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=FutureWarning, module='gensim')


class load_model():

  def __init__(self):
    self.dictionary = object 
    #self.corpus = object
    self.model_TFIDF = object
    #self.corpus_TFIDF = object
    self.index_TFIDF = object
    self.model_LSI = object
    #self.corpus_LSI = object
    self.index_LSI = object    

  def load_all_models(self, modelname):

    disk = disk_access()       
    self.dictionary =  corpora.Dictionary.load(disk.get_model_absolute_path(modelname + ".dict"))
    self.model_TFIDF =  models.TfidfModel.load(disk.get_model_absolute_path(modelname + ".tfidf")) 
    self.index_TFIDF =  similarities.MatrixSimilarity.load(disk.get_model_absolute_path(modelname + "_tfidf.index")) 
    self.model_LSI =  models.LsiModel.load(disk.get_model_absolute_path(modelname + ".lsi"))
    self.index_LSI =  similarities.MatrixSimilarity.load(disk.get_model_absolute_path(modelname + "_lsi.index"))
    
  