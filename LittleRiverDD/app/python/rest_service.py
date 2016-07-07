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
from functools import wraps
import json
import os
import arcpy
from _structures import *
from flask_utils import collect_args, support_jsonp
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from llrd import utils
from datetime import datetime

def convertDate(date_str):
    """converts string in this format MM/DD/YYYY to datetime object"""
    m,d,y = date_str.split('/')
    return datetime(*map(int, [y,m,d]))

FIELD_MAP = {"esriFieldTypeString": str,
             "esriFieldTypeOID": int, # will auto convert to long if necessary
             "esriFieldTypeSmallInteger": int,
             "esriFieldTypeSingle": float,
             "esriFieldTypeDouble": float,
             "esriFieldTypeDate": convertDate,
        }

f_dict = {f['name']: f for f in FIELD_OBJECTS}
FIELD_INDEX_MAP = {f:i for i,f in enumerate(FIELDS)}

app = Flask(__name__)
gdb = utils.Geodatabase()

fc = gdb.summary_table

def fetch_records(where=''):
    """queries the database to build json cache

    Optional:
        where -- where clause for cursor
    """
    print where
    with arcpy.da.SearchCursor(fc, FIELDS, where_clause=where) as rows:
        records = [{'attributes': dict(zip(FIELDS, r))} for r in rows]
        setattr(sys.modules[__name__], 'records', records)
        return records

records = {}
owners = {}

def cast(field, value):
    """casts to appropriate type based on field name and type"""
    if field == 'OBJECTID':
        return int(value)
    if value in ('null', None):
        return None
    try:
        return FIELD_MAP[f_dict[field]['type']](value)
    except:
        return None

def fetch_owner_summary(where=''):
    owners = gdb.get_admin_fees(where)
    setattr(sys.modules[__name__], 'owners', owners)
    return owners

def check(k, v, test):
    """checks input to test if condition is met

    k -- key to search for
    v -- actual attribute value
    test -- condition to test if matches v
    """
    if not k or test is None or v is None:
        return False
    if k in ('OWNER', 'COUNTY'):
        return str(test).upper() in v
    else:
        return test == v

def query_records(**kwargs):
    """generic lazy query, use kwargs to match field names"""
    recs = []
    for ft in records:
        if all(check(k.upper(), ft['attributes'][k.upper()], kwargs[k.lower()])
               for k in kwargs.keys() if k.upper() in FIELDS):
            recs.append(ft)
    return recs

@app.route('/rest/counties', methods=['GET', 'POST'])
@support_jsonp
def get_counties():
    """get a list of counties"""
    return jsonify(COUNTIES)

@app.route('/rest/fields', methods=['GET', 'POST'])
@support_jsonp
def get_fields():
    """get field objects"""
    return jsonify(FIELD_OBJECTS)

@app.route('/rest/fieldNames', methods=['GET', 'POST'])
@support_jsonp
def get_fieldNames():
    """gets field names only"""
    return jsonify(FIELDS)

@app.route('/rest/fieldAliases', methods=['GET', 'POST'])
@support_jsonp
def get_fieldAliases():
    """gets field aliases"""
    return jsonify(FIELD_ALIASES)

@app.route('/rest/features', methods=['GET','POST'])
@support_jsonp
def get_features():
    """gets all features from json cache"""
    return jsonify(records)

@app.route('/rest/byCode', methods=['GET','POST'])
@support_jsonp
def get_code():
    """Gets owners by Code

    Parameters:
        code -- owner code
    """
    recs = []
    arg = request.args.get('code', '', type=str).upper()
    for ft in records:
        if ft['attributes']['OWNER_CODE'] == arg:
            recs.append(ft)

    return jsonify(recs)

@app.route('/rest/byPIN', methods=['GET','POST'])
@support_jsonp
def get_pin():
    """Gets owner by PIN

    Parameters:
        pin -- search for parcel ID with no special characters
    """
    recs = []
    arg = request.args.get('pin', '', type=str)
    for ft in records:
        if ft['attributes']['PIN'] == arg:
            recs.append(ft)

    return jsonify(recs)

@app.route('/rest/byName', methods=['GET','POST'])
@support_jsonp
def get_name():
    """Gets owners by name

    Parameters:
        name -- name of owner (returns any string that CONTAINS this string)
    """
    recs = []
    arg = request.args.get('name', '', type=str).upper()
    for ft in records:
        if arg in ft['attributes']['OWNER']:
            recs.append(ft)

    return jsonify(recs)

@app.route('/rest/byCounty', methods=['GET','POST'])
@support_jsonp
def get_county():
    """Gets all owners within a county

    Parameters:
        county -- name of county
    """
    return jsonify(query_records(**request.args.to_dict()))

@app.route('/rest/query', methods=['GET','POST'])
@support_jsonp
def do_query():
    """Performs a query using multiple fields on the cached json

    Parameters:
        amount_paid  -- total amount paid
        assessed_acres -- assessed acres
        county -- name of county
        date_paid -- date paid (in miliseconds)
        excess -- excess paid
        flag -- flagged record
        objectid -- object id
        owner -- owner name
        owner2 -- owner name 2
        owner_code --- owner code
        parcel_id -- parcel id
        penalty -- penalty amount
        pin -- pin with no special characters
        range -- range as z fill (examples: 07, 13)
        sec_twn_rng -- section-township-range with 2 character z-fill (ex: 01-04-16)
        section -- section as z fill (examples: 07, 13)
        sequence -- sequence
        tot_admin_fee -- total admin fee
        tot_assessment -- total assessment
        tot_benefit -- tot_benefit
        township -- township as z fill (examples: 07, 13)
        year -- tax year (YYYY)
    """
    return jsonify(query_records(**request.args.to_dict()))

@app.route('/rest/applyEdits', methods=['POST', 'GET'])
@support_jsonp
def applyEdits():
    """ This operation supports POST operations only, a header should also
    be included for the content type {Content-Type: application/json}.

    Parameters:
        updates -- records to be updated
    """
    data = collect_args()
    updates = json.loads(data.get('updates', '[]'))
    adds = json.loads(data.get('adds', '[]'))
    deletes = json.loads(data.get('deletes', '[]'))
    print updates, 'updates, ', bool(updates), type(updates)
    print deletes, 'deletes, ', bool(deletes), type(deletes)
    print 'adds, ', adds, bool(adds), type(adds)
    if bool(updates) or bool(deletes):
        pin_index = FIELDS.index('PIN')
        oid_index = FIELDS.index('OBJECTID')

        # create dict for updates
        upd = {u['PIN']: u for u in updates}
        pin_tup = tuple(str(p) for p in upd.keys()) if len(upd.keys()) > 1 else "('{}')".format(upd.keys()[0])
        where = "PIN IN {}".format(pin_tup)
        with arcpy.da.UpdateCursor(fc, FIELDS, where) as rows:
            for r in rows:
                pin = r[pin_index]
                if pin in upd:
                    vals = upd[pin]
                    for f, value in vals.iteritems():
                        #print f, value
                        if f not in ('OBJECTID', 'PIN'):
                            r[FIELD_INDEX_MAP[f]] = cast(f, value)
                    rows.updateRow(r)
##                elif r[oid_index] in deletes:
##                    rows.deleteRow()

    # do adds
    insert_fields = [f for f in FIELDS if f != ['OBJECTID']]
    with arcpy.da.InsertCursor(fc, insert_fields) as irows:
        for atts in adds:
            row = [None] * len(insert_fields)
            for f, value in atts.iteritems():
                if f not in ('newRecord', 'OBJECTID'):
                    row[FIELD_INDEX_MAP[f]] = cast(f, value)
            irows.insertRow(row)

    status={'status': 'success',
            'results': {
                'adds': len(adds),
                'updates': len(updates),
                'deletes': len(deletes)
            }
        }

    # rehydrate the cache of records
    fetch_records()
    return jsonify(status)

@app.route('/rest/getOwnerSummary', methods=['GET', 'POST'])
@support_jsonp
def getOwnerSummary():
    args = collect_args()
    if args.get('code') in owners:
        return jsonify(owners[args.get('code')])
    return jsonify({})

@app.route('/rest/getAllOwnerSummaries', methods=['GET', 'POST'])
@support_jsonp
def getAllOwnerSummaries():
    return jsonify(owners.values())

@app.route('/rest/fetch', methods=['GET','POST'])
@support_jsonp
def do_fetch():
    """Will rehydrate the json cache or will set cache to only a subset of records

    Parameters:
        where -- where clause for cursor to fetch new json cache
    """
    arg = request.args.get('where', '', type=str)
    recs = fetch_records(arg)
##    setattr(sys.modules[__name__], 'records', recs)
    return jsonify(recs)

@app.route('/rest/fetchOwners', methods=['GET','POST'])
@support_jsonp
def fetchOwners():
    """Will rehydrate the json cache or will set cache to only a subset of records

    Parameters:
        where -- where clause for cursor to fetch new json cache
    """
    arg = request.args.get('where', '', type=str)
    recs = fetch_owner_summary(arg)
##    setattr(sys.modules[__name__], 'records', recs)
    return jsonify(recs)

if __name__ == '__main__':

    # set up records
    fetch_records()
    fetch_owner_summary()

    # run REST service
    app.run(port=5001, debug=True)

