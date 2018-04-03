#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# #      Created Date: Mon Mar 19 2018
# #      Author: Ryan
# #      mail: ryan.netx@outlook.com
# #      Last Modified:
# #      Modified By:
# #------------------------------------------
# #      Copyright (c) 2018
# #------------------------------------------
# #
###
from flask import Flask, render_template, request, url_for
from flask_restful import Api, Resource
import getProxyIP

app = Flask(__name__)
api = Api(app)

UPDATETIME = 180
UPDATEFLAG = 0


def updatetime():
    while 1:
        global UPDATEFLAG
        UPDATEFLAG = 0
        getProxyIP.sleep(UPDATETIME)


class UpdateProxyIP(Resource):
    def get(self):
        global UPDATEFLAG
        if UPDATEFLAG == 0:
            UPDATEFLAG = 1
            print('update')
            getProxyIP.pxiplist = []
            pxiplist = getProxyIP.getVIVDPX('proxy.json')
            with open('proxyvivdip.json', 'w', encoding='utf-8') as f:
                getProxyIP.json.dump(pxiplist, f)
            return {'status': '0'}, 200
        else:
            print('no update')
            return {'error': 'refresh in 3 min later'}, 400


@app.route('/')
@app.route('/index')
def index():
    with open('proxyvivdip.json', encoding='utf-8') as f:
        msg = getProxyIP.json.load(f)
    total = len(msg)
    ip = request.remote_addr
    return render_template('index.html', msg=msg, total=total, ip=ip), 200


static', filename='favicon.ico'))
api.add_resource(UpdateProxyIP, '/api/updateproxyip')

if __name__ == '__main__':
    t=getProxyIP.Thread(target=updatetime)
    t.start()
    app.run(host='127.0.0.1', port=9999, threaded=True)
    # app.run(host='127.0.0.1', port=9999, debug=True, threaded=True)
