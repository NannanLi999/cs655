import flask
from flask import Flask, request, send_from_directory, jsonify

from flask import Response
from flask_cors import CORS

import requests


app = Flask(__name__, static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

@app.route('/')
def init_page():    
    return send_from_directory('./templates/','index.html') 

@app.route('/get_pred', methods=['GET', 'POST'])
def get_pred():
    if request.method == "POST":
        caption = request.form['caption']

        session = requests.Session()
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload = {'caption': caption}
        
        print(payload)
        x = session.post('http://143.215.216.193:5002/get_pred', headers=headers,data=payload)
        
        print(x.json())
        if x.status_code == 200:
            return jsonify(x.json())
        else:
            error_data = {
                'sentiment': "error"
            }
        return jsonify(error_data)

if __name__=="__main__":
    app.run(debug=False, host='0.0.0.0', port="5002")
