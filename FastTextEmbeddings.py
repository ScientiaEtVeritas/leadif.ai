from gensim.models import KeyedVectors
import nltk
import numpy as np

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
                vectors.append(model.get_vector(token.lower()))
            except:
                pass
        return vectors

    def getMeanEmbedding(self):
        return np.array(FastTextEmbeddings._getVectorsOf(self.tokens)).mean(axis=0)