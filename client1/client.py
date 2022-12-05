import argparse
import requests

def send_request(msg):
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload= {'caption':msg} 
    try:
        session = requests.Session()
        response = session.post('http://143.215.216.195:5002/get_pred', headers=headers,data=payload,timeout=1)
        if response.status_code==200:
            res=response.json()['sentiment']
            if abs(res['pos']-res['neg'])<0.1:
               print("Neutral")
            elif res['pos']>res['neg']:
               print("Positive")
            else:
               print("Negative")   
        
    except:
       print("Package is lost. Please resend.")

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Echo server')
    parser.add_argument('--msg', '--message', default='It\'s a sunny day.', type=str, help='Input text.')
    args = parser.parse_args()
    send_request(args.msg)
