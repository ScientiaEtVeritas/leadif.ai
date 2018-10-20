from gensim.models import KeyedVectors
import nltk
import numpy as np
import re

model = KeyedVectors.load_word2vec_format('wiki.de.vec')

class FastTextEmbeddings():
    def __init__(self, text):
        self.text = text
        self.tokens = nltk.word_tokenize(text)

    @staticmethod
    def _getVectorsOf(tokens):
        vectors = []
        for token in tokens:
            try:
                print(re.sub('[^A-Za-z0-9]+', '', token))
                vectors.append(model.get_vector(re.sub('[^A-Za-z0-9]+', '', token).lower()))
            except:
                print(token)
                pass
        return vectors

    def getMeanEmbedding(self):
        return np.array(FastTextEmbeddings._getVectorsOf(self.tokens)).mean(axis=0)