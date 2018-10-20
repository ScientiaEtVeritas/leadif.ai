from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from ParagraphEmbedding import ParagraphEmbedding

app = Flask(__name__)
CORS(app)

@app.route('/get', methods=['GET'])
def classify_url():
    print(ParagraphEmbedding(request.args.get('url')).getMeanEmbedding()[0])
    return jsonify({'result': "bla"})

if __name__ == '__main__':
    app.run(debug=True, port=8092, use_reloader=False)
