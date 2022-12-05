import requests
import time
import numpy as np
import json
from multiprocessing import Pool
from multiprocessing import freeze_support
import matplotlib.pyplot as plt

NUM_EXP=100
OK=200
LOST=101

caption=['I\'m tall.','Things are getting better.','Python combines remarkable power with very clear syntax.']


def run_client(n):
        result = {'lost':None,'status':None,'time':None,'size':None}  
        headers = {'User-Agent': 'Mozilla/5.0'}
        payload= {'caption':np.random.choice(caption)} 
        t1=time.time() 
        session = requests.Session()
        times=[]
        sizes=[]
        num_lost=0
        status=LOST
        for _ in range(NUM_EXP):
          try:
            response = session.post('http://143.215.216.195:5002/get_pred', headers=headers,data=payload,timeout=1)
            if response.status_code==200:
                #response = response.json()
                t2=time.time()
                json_string=json.dumps(payload)
                bytes=json_string.encode("utf-8")
                times.append(t2-t1)
                #result['status']=OK
                status=OK
                sizes.append(len(bytes)) 
          except:
                num_lost+=1
        result['status']=status
        result['size']=np.sum(sizes)
        result['time']=np.mean(times)
        result['lost']=num_lost
        return result

def run_multiprocessing(func, i, n_processors):
    with Pool(processes=n_processors) as pool:
        return pool.map(func,i)

if __name__ == '__main__':
    freeze_support()

    num_req_choices=[5*i for i in range(1,11)]
    all_tput = []
    all_rtt = []
    all_loss = []
    for num_req in num_req_choices:
           headers = {'User-Agent': 'Mozilla/5.0'}
           rtts=[]
           num_loss=0

           sent_data_size=0
           start_time = time.time()

           result_list = run_multiprocessing(run_client, [0]*num_req, num_req)
           for result in result_list: 
               if result['status']==OK:
                   rtts.append(result['time'])  
                   sent_data_size+=result['size']
                   num_loss+=result['lost']
               else:
                   num_loss+=result['lost']
           end_time = time.time()
           tput = sent_data_size/(end_time-start_time)
           all_tput.append(tput)
           all_rtt.append(np.mean(rtts))
           all_loss.append(num_loss/(num_req*NUM_EXP))
           print("=========num_req = %d====="%num_req)
           print("throughput: %.2f bps"%tput)
           print("ave rtt: %.2f seconds"%np.mean(rtts))
           print("loss ratio: %.2f"%(num_loss/(num_req*NUM_EXP)))
    names=['RTT','Throughput','Loss']
    plt.figure()
    for i,y in enumerate([all_rtt,all_tput,all_loss]):
        plt.xlabel('number of clients')
        plt.ylabel(names[i])
        plt.title(names[i])
        plt.plot(num_req_choices,y)
        plt.tight_layout()
        plt.savefig('./'+names[i]+'.png')
        plt.clf()



