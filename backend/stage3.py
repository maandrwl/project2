from flask import Flask, request
import requests
from flask import json, jsonify
import os
from stage3Java import compileJava
from stage3Python import compilePython 
import api_urls
import shutil

PATH = os.path.dirname(os.path.abspath(__file__))
PATH_MAIN = os.path.join(os.path.dirname(PATH), 'app')
app = Flask(__name__)
STAGE4 = api_urls.BASE_URL_STAGE4
queueFolder = ['1','2','3','4','5','6','7','8','9','10']
if os.listdir(os.path.join(PATH_MAIN, 'store_output')):
    shutil.rmtree(os.path.join(PATH_MAIN, 'store_output'), ignore_errors=True)
os.makedirs(os.path.join(PATH_MAIN, 'store_output'), exist_ok=True)


@app.route('/stage3J', methods=['POST'])
def stage3J():
    dictdata = request.get_json(force=True)
    java = compileJava(dictdata, PATH_MAIN, queueFolder.pop(0))
    java.runWork()
    work, fStage4 = java.getWork()
    if(work['status']['boolean']):
        print('go to stage 4')
        score = requests.post(STAGE4, json=fStage4)
        score = json.loads(score.content)
        FolderOut = score['queueFolder']['PATH_OUTPUT']
        queueOut = score['queueFolder']['queueFolder']
        queueFolder.append(queueOut)
        shutil.rmtree(FolderOut, ignore_errors=True)
        work.update(score)
        print('end stage 4')
        print('------')
    requests.post(dictdata['data']['apiFinal'], json=work)
    return work

@app.route('/stage3P', methods=['POST'])
def stage3P():
    dictdata = request.get_json(force=True)
    python = compilePython(dictdata, PATH_MAIN, queueFolder.pop(0))
    python.runWork()
    work, fStage4 = python.getWork()
    if(work['status']['boolean']):
        print('go to stage 4')
        score = requests.post(STAGE4, json=fStage4)
        score = json.loads(score.content)
        FolderOut = score['queueFolder']['PATH_OUTPUT']
        queueOut = score['queueFolder']['queueFolder']
        queueFolder.append(queueOut)
        shutil.rmtree(FolderOut, ignore_errors=True)
        work.update(score)
        print('end stage 4')
        print('------')
    requests.post(dictdata['data']['apiFinal'], json=work)
    return "hello"

if __name__ == '__main__':
    app.run(debug=True, host= api_urls.local_ip, port=5002)