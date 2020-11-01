import nltk
import os
import logging
import tensorflow as tf
from google.cloud import storage


nltk.download('punkt')
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
tf.config.experimental.set_visible_devices(devices= my_devices, device_type='CPU')


def create_tokens_tensor(text, tokenizer):
    """ Creates tokens tensor and list of masked word indexes.
    Args:
        text (str): A sequence of text containing masked words to be predicted.
        tokenizer (obj): A tokenizer to process input text.
    Returns:
        obj: Tensorflow tensor of tokenized text.
        list: Masked word indexes
    """
    
    # Remove whitespace if present at the end of the sentence.
    text = text.rstrip()
    
    # Add puntuation if not present at end of text.
    punctuation = '.!?'
    
    if text[-1] not in punctuation:
      split_text = text.split()
      five_W_one_H = ['who', 'what', 'where', 'when', 'why', 'how', 'is']
      first_word = split_text[0]
      if first_word.lower() in five_W_one_H:
        text += '?'
      else:
        text += '.'

    # Replace all occurances of 'unk' with [MASK]
    text_replace = text.replace('unk', '[MASK]')

    # Split the text into a list of sentences.
    split_sequence = nltk.sent_tokenize(text_replace)

    # Join text for encoding
    join_text = ' '.join(split_sequence) 

    # Create inputs for model by adding special tokens and encoding text. 
    input_ids = tokenizer.encode(join_text)

    # Create list of indexes for masked words.
    masked_index_list = [i for i, input_id in enumerate(input_ids) if input_id == 103]

    # Turn input_ids into tensor
    tokens_tensor = tf.constant([input_ids])
    return text, tokens_tensor, masked_index_list



def make_predictions(tokens_tensor, masked_index_list, tokenizer, model):
    """ Makes predictions for masked words.
    Args:
        tokens_tensor (obj): Tensorflow tensor of tokenized text.
        masked_index_list (list): List of masked word indexes obtained after encoding.
        tokenizer (obj): Tokenizer for specified model.
        model (obj): NLP model to make predictions.
    Returns:
        list: Predicted word(s) for masked inputs.
    """
    # Process input_ids.
    outputs = model(tokens_tensor)
    # Get predictions from output.
    predictions = outputs[0]
    # Take argmax of predictions.
    predicted_max = [tf.math.argmax(predictions[0, masked_index]) for masked_index in masked_index_list]
    # Convert predictions back to text.
    predicted_tokens = [tokenizer.convert_ids_to_tokens([prediction])[0] for prediction in predicted_max]
    return predicted_tokens


def download_blob(project, bucket_name, prefix, dl_dir):
    """ Downloads blobs from Google Cloud Storage.
    Args:
        bucket_name (str): GCS bucket name.
        prefix: Local destination prefix.
        dl_dir: Destination directory.
        filename: name of file to be downloaded.
    """
    if not os.path.exists(f'{dl_dir}/{prefix}'):
        os.makedirs(f'{dl_dir}/{prefix}')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)  # Get list of files
    for blob in blobs:
        logging.info(f'Blobs: {blob.name}')
        blob.download_to_filename(f'{dl_dir}/{blob.name}')
