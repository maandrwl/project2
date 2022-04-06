from flask import Flask, request
import requests
from stage4J import judge
import os
import api_urls

app = Flask(__name__)

@app.route('/stage4', methods=['POST'])
def stage4():
    print('working stage 4')
    dictdata = request.get_json(force=True)
    score = judge(dictdata)
    if dictdata['format']:
        score.judgeFormat()
    else:
        score.judgeUnFormat()
    total = score.getScore()
    return total

if __name__ == '__main__':
    app.run(debug=True, host= api_urls.local_ip, port=5003)