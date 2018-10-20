from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/get', methods=['GET'])
def classify_url():
    return jsonify({'result': request.args.get('text')})

if __name__ == '__main__':
    app.run(debug=True, port=8090, use_reloader=False)
