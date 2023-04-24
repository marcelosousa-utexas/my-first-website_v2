
import os, warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=FutureWarning, module='gensim')
#from gensim import corpora, models, similarities
from gensim import corpora

class build_model():

  def __init__(self):
    print("init class")
  
  def write_dict(self, parameter_value_list):
    print(parameter_value_list)
    dictionary = corpora.Dictionary(parameter_value_list)
    print(os.environ['DISK_FOLDER'] + 'dicionario_palavras_chave.dict')
    #dictionary.save('/var/data/models/dicionario_palavras_chave.dict')
    dictionary.save(os.environ['DISK_FOLDER'] + 'dicionario_palavras_chave.dict')