from flask import Flask, request
import requests
import os
from queue import Queue
from stage2Q import manageQ
import json
from AfterResponse import AfterResponse
import api_urls
import threading

PATH_MAIN = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
AfterResponse(app)
STAGE3 = api_urls.BASE_URL_STAGE3

Q = manageQ()

# @app.after_response
def loopWork():
    # if not Q.qEmpty():
    x = 0
    while not Q.qEmpty():
        print(x)
        print('PQ --->', Q.getpQueue())
        print('CQ --->', Q.getcQueue())
        data = Q.sentQueue()
        print('DQ --->', data['data']['Queue'])
        print('go to stage 3')
        try:
            requests.request("POST", data['data']['API'], json=data)
        except:
            pass
        # work = requests.post(data['data']['API'], json=data)
        print('end stage 3')
        # dictdata = json.loads(work.content)
        # requests.post(dictdata['data']['apiFinal'], json=dictdata)
        Q.setpQueue()
        print('get q --->', Q.getpQueue())
        x = x+1

@app.route('/stage2', methods=['POST'])
def stage2():
    dictdata = request.get_json(force=True)
    dictdata['data']['API'] = STAGE3 + Q.getAPI(dictdata['data']['language'])
    queue = str(Q.setcQueue())
    dictdata['data']['Queue'] = queue
    Q.putQ(dictdata)
    print('PQ --->',Q.getpQueue())
    print('CQ --->',Q.getcQueue())
    if Q.checkQ(int(dictdata['data']['Queue'])):
        print('run thread')
        thread = threading.Thread(target=loopWork)
        thread.start()
    return dictdata['data']['Queue']

if __name__ == '__main__':
    app.run(debug=True, host= api_urls.local_ip, port=5001)