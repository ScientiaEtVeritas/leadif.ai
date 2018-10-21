import os
import asyncio
from flask import Flask, jsonify, request
from flask_cors import CORS
from ParagraphEmbedding import ParagraphEmbedding
from FastTextEmbeddings import FastTextEmbeddings
from parser import ParseWebsite
from screenshot import screenshot
from wikipedia_info import Wikipedia

app = Flask(__name__)
CORS(app)

def handle_website_data(url):
    parser = ParseWebsite(url)
    text = parser.get_text()
    social_media = parser.get_all_links()
    embedding = FastTextEmbeddings(text).getMeanEmbedding()[0]
    return  {'social_media': social_media, 'embedding': embedding}

def handle_wikipedia_data(url):
    wiki = Wikipedia(url)
    wiki_data = wiki.getInfoBoxAsDict()
    embedding = ''

    resultset = [value for key, value in wiki_data.items() if key not in ['content']]

    return {'ui_info': resultset, 'embedding': embedding }

def make_screenshot(url):
    asyncio.get_event_loop().run_until_complete(screenshot(url))


@app.route('/get', methods=['GET'])
def classify_url():
    url = request.args.get('url')

    website_data = handle_website_data(url)

    return jsonify({'social': website_data['social_media']})

if __name__ == '__main__':
    app.run(debug=True, port=8092, use_reloader=False)
