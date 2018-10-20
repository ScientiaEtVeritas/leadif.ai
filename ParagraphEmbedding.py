import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import nltk

embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")

class ParagrapgEmbedding():
    def __init__(self, text):
        self.text = text
        self.sentences = nltk.sent_tokenize(text)

    def getMeanEmbedding(self):
        embeddings = embed(self.sentences)
        mean_embedding = tf.reduce_mean(embeddings, axis=0) 
        with tf.Session() as session:
            session.run([tf.global_variables_initializer(), tf.tables_initializer()])
            mean_embedding = session.run(mean_embedding)
        self.mean_embedding = mean_embedding
        return self.mean_embedding

    @staticmethod
    def getDistanceBetween(embedding_a, embedding_b):
        corr = np.inner(embedding_a, embedding_b)
        return corr
    
