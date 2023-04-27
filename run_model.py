import re
from unicodedata import normalize
import os
import nltk
nltk.data.path.append(os.getcwd() + os.sep  + "nltk_data")
from nltk import corpus
from nltk import regexp_tokenize



class classifier_model():
  
  def __init__(self, data, dictionary, model_TFIDF, index_TFIDF, model_LSI, index_LSI):
    self.data = data
    self.dictionary = dictionary
    self.model_TFIDF = model_TFIDF
    self.index_TFIDF = index_TFIDF
    self.model_LSI = model_LSI
    self.index_LSI = index_LSI

  def start_classifier_model(self):

        model_result = []
        data = normalize('NFKD', self.data).encode('ASCII','ignore').decode('ASCII')
        data = re.split("\\f", data)

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
                
                        find_classification = [page_number, document_type, best_fit_tfidf_model,tfidf_alert, best_fit_lsi_model, lsi_alert]                        
                        model_result.append(find_classification)
        return model_result