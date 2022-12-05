import flask
from flask import Flask, request, send_from_directory, jsonify
from flask import Response
from flask_cors import CORS
# from transformers import GPT2Tokenizer, GPT2LMHeadModel
# import torch
from nltk.sentiment import SentimentIntensityAnalyzer
import time

import random

app = Flask(__name__, static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#model = GPT2LMHeadModel.from_pretrained("gpt2")#)'./src/checkpoint/')
#model.to(device)

#tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#tokenizer.sos_token = '<sos>'
#tokenizer.eos_token = '<eos>'
#tokenizer.pad_token = '<pad>'

#preprocess = lambda caption, emotion: f"<sos> The news caption: {caption}, would invoke the emotions: {emotion}, because the reader would think: " 
#postprocess = lambda generation: generation.split('<eos>')[0].split('think:')[-1].strip()

#def inference(caption, emotion):
#    text = preprocess(caption, emotion)
#    input_ids = tokenizer.encode(text, return_tensors='pt')
#    input_ids = input_ids.to(device)

#    beam = postprocess(tokenizer.decode(model.generate(input_ids, 
#                       max_length=200, num_beams=5, no_repeat_ngram_size=2, 
#                       early_stopping=True, pad_token_id=50256)[0])) # beam search

#    return beam

sia = SentimentIntensityAnalyzer()

@app.route('/get_pred', methods=['GET', 'POST'])
def get_prediction():
    if request.method=="POST":
        caption = request.form['caption']

        sentiment = sia.polarity_scores(caption)
        
        # simluate server error/hang
        if random.random()>0.9:
            time.sleep(10)
        print(caption, sentiment)
        data = {
            'caption': caption,
            'sentiment': sentiment
        }
        print(data)
        return jsonify(data)

if __name__=="__main__":
    app.run(debug=False, host='0.0.0.0', port="5002")


