from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/get', methods=['GET'])
def classify_url():
    return jsonify({'result': request.args.get('url')})

if __name__ == '__main__':
    app.run(debug=True, port=8090, use_reloader=False)
