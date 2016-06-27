#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     24/06/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from flask import Flask, request, jsonify, abort
import json
import os
from . import utils

app = Flask(__name__)

path = r'E:\inetpub\wwwroot\lrrd\summary.json'

with open(path, 'r') as f:
    rc = json.load(f)

records = rc['features']

@app.route('/flask/api/features', methods=['GET','POST'])
def get_features():
    return jsonify(records)

@app.route('/flask/api/byCode', methods=['GET','POST'])
def get_code():
    recs = []
    arg = request.args.get('code', '', type=str).upper()
    for ft in records:
        if ft['attributes']['OWNER_CODE'] == arg:
            recs.append(ft)

    return jsonify(recs)

@app.route('/flask/api/byPIN', methods=['GET','POST'])
def get_pin():
    recs = []
    arg = request.args.get('pin', '', type=str)
    for ft in records:
        if ft['attributes']['PIN'] == arg:
            recs.append(ft)

    return jsonify(recs)

@app.route('/flask/byName', methods=['GET','POST'])
def get_name():
    recs = []
    arg = request.args.get('name', '', type=str).upper()
    for ft in records:
        if arg in ft['attributes']['OWNER']:
            recs.append(ft)

    return jsonify(recs)

if __name__ == '__main__':
    app.run(port=5000, debug=True)

