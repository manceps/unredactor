#! /env/bin/python3

import os
import subprocess
import logging

from flask import Flask, request
from flask_cors import CORS
from waitress import serve

from transformers import DistilBertTokenizerFast, TFDistilBertForMaskedLM 
from unredactor_service import create_tokens_tensor, make_predictions, download_blob

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)


project = os.environ.get('PROJECT')
bucket_name = os.environ.get('BUCKET_NAME')
prefix = os.environ.get('PREFIX', default='')
user = os.environ.get('USER')
download_dir = os.environ.get('DOWNLOAD_DIR', default=f'/home/{user}')
tokenizer_path = os.environ.get('TOKENIZER_PATH', default='tokenizer/')
model_path = os.environ.get('MODEL_PATH', default='model/')


logging.info('Downloading tokenizer and model files...')

download_blob(project, bucket_name, tokenizer_path, download_dir)
download_blob(project, bucket_name, model_path, download_dir)

logging.info('Loading tokenizer and model...')
tokenizer = DistilBertTokenizerFast.from_pretrained(f'{download_dir}/{tokenizer_path}')
model = TFDistilBertForMaskedLM.from_pretrained(f'{download_dir}/{model_path}')

@app.route('/unredact', methods=['POST'])
def unredactor():
    content = request.get_json()
    text = content['text']

    # Create tokens tensor and list of masked word indexes
    text, tokens, index_list = create_tokens_tensor(text, tokenizer)

    # Make list of predictions for masked words.
    predictions = make_predictions(tokens, index_list, tokenizer, model)

    return {"predictions": predictions}

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=os.environ.get('PORT', 8080))
