import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import nltk

g = tf.Graph()
with g.as_default():
    embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")

class ParagraphEmbedding():
    def __init__(self, text):
        self.text = text
        self.sentences = nltk.sent_tokenize(text)

    def getMeanEmbedding(self):
        with g.as_default():
            embeddings = embed(self.sentences)
            mean_embedding = tf.reduce_mean(embeddings, axis=0) 
            init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
        with tf.Session(graph=g) as session:
            session.run(init_op)
            mean_embedding = session.run(mean_embedding)
        self.mean_embedding = mean_embedding
        return self.mean_embedding

    @staticmethod
    def getDistanceBetween(embedding_a, embedding_b):
        corr = np.inner(embedding_a, embedding_b)
        return corr
    
