import gensim.downloader as api
import nltk
import numpy as np

model = api.load("glove-wiki-gigaword-300")

class GloVeEmbeddings():
    def __init__(self, text):
        self.text = text
        self.tokens = nltk.wordpunct_tokenize(text)

    @staticmethod
    def _getVectorsOf(tokens):
        vectors = []
        for token in tokens:
            try:
                vectors.append(model[token])
            except:
                pass
        return vectors

    def getMeanEmbedding(self):
        return np.array(GloVeEmbeddings._getVectorsOf(self.tokens)).mean(axis=0)
