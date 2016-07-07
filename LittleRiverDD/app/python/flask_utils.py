#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     26/06/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from flask import request, jsonify, current_app
from functools import wraps
import json

class AuthBMI(object):
    pass


def support_jsonp(f):
    """Wraps JSONified output for JSONP

    https://gist.github.com/aisipos/1094140
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function

def collect_args():
    """collects arguments from either query string OR request body and returns as
    dictionary for server side processing
    """
    # check query string first
    data = {}
    for arg in request.values:
        val = request.args.get(arg, None)
        if val is not None:
            data[arg] = val

    if not data:
        data = request.form

    # check data as fallback
    if not data:
        data = request.get_json()
        if data is None:
            # no application/json mimetype header...
            try:
                data = json.loads(request.data)
            except:
                data = {}

    return data