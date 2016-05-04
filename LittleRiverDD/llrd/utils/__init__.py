#-------------------------------------------------------------------------------
# Name:        Utilities
# Purpose:     Little River Drainage District Utilites
#
# Author:      Caleb Mackey
#
# Created:     02/24/2016
# Copyright:   (c) Bolton & Menk, Inc. 2016
#-------------------------------------------------------------------------------
import arcpy
import os
import time
import datetime
import json
import sys
import traceback
import fnmatch
import shutil
import zipfile
import ftplib
import logging
from collections import OrderedDict

# custom imports
try:
    SOURCE_DIR = os.path.dirname(os.path.dirname(__file__))
except:
    SOURCE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))

sys.path.append(os.path.join(SOURCE_DIR, 'thirdParty'))

# local imports
import munch

# constants
THIRD_PARTY = os.path.join(SOURCE_DIR, 'thirdParty')
BIN = os.path.join(SOURCE_DIR, 'bin')
DATA = os.path.join(BIN, 'data')
CONFIG = os.path.join(BIN, 'config.json')
PARCEL_FIELDS = os.path.join(BIN, 'parcel_fields.json')
PARCEL_LR_FIELDS = os.path.join(BIN, 'lr_fields.json')
OWNER_CODE = 'OWNER_CODE'
PARCEL_ID = 'PARCEL_ID'
PIN = 'PIN'
SEC_TWN_RNG = 'SEC_TWN_RNG'

LAST_YEAR = datetime.datetime.now().year - 1

# ArcGIS environments
arcpy.env.overwriteOutput = True

__all__ = ['BIN', 'DATA', 'CONFIG', 'PARCEL_FIELDS', 'PARCEL_ID', 'Message', 'fixGpArgs', 'parseValueTable',
           'ErrorLog', 'toolLog', 'timeit', 'passArgs', 'zipdir', 'unzip', 'assignUniqueName', 'getConfig',
           'getParcelConfig', 'getParcelFields', 'getFieldMapDict', 'getTemplate', 'writeConfig', 'field_mappings',
           'Geodatabase', 'Owner', 'LandOwners', 'getPIN', 'UpdateCursor', 'InsertCursor']

#******************************************************************************************************************************
#
# Tool helper functions
def Message(*args):
    """
    Prints message to Script tool window or python shell

    msg: message to be printed
    """
    if isinstance(args, (list, tuple)):
        for msg in args:
            print str(msg)
            arcpy.AddMessage(str(msg))
    else:
        print str(msg)
        arcpy.AddMessage(str(msg))

def fixGpArgs():
    """
    fixes arguments from a script tool.  for example,
    when using a script tool with a multivalue parameter,
    it comes in as "val_a;val_b;val_c".  This function can
    automatically fix arguments based on the arg_type.

    Another example is the boolean type returned from a
    script tool.  Instead of True and False, it is returned as
    "true" and "false"

    # Example:
    >>> # example of list returned from script tool multiparameter argument
    >>> arg = "val_a;val_b;val_c" #format from script tool
    >>> fixArgs()
    ['val_a', 'val_b', 'val_c']
    """
    stringTypes = ['file', 'folder', 'string', 'feature class', 'field', 'workspace',
                'any value', 'area units', 'linear unit', 'dbase table', 'shapefile', 'feature dataset',
                'arcmap document', 'cad drawing dataset','raster catalog', 'raster dataset', 'pyramid',
                'raster band', 'topo features', 'topology', 'valuetable', 'vertical factor', 'vpf coverage',
                'vpf table']

    Message('Fixing GP Args')
    args = [arcpy.GetParameter(i) for i in range(arcpy.GetArgumentCount())]
    fixedArgs = []
    params = arcpy.GetParameterInfo()
    pInfo = tuple([a, params[i].datatype, params[i].multiValue] for i, a in enumerate(args))

    pInfoPrint = tuple(p[:] for p in pInfo)
    for l in pInfoPrint:
    	if l[1] == 'String Hidden':
    		l[0] = '*******'

    Message(pInfoPrint) # hide hidden strings

    for arg, arg_type, isMulti in pInfo:
        # handle multi value params first
        if isMulti:
            cast = str
            if arg_type == 'Long':
                cast = int
            elif arg_type == 'Double':
                cast = float
            if isinstance(arg, basestring):
                if str(arg) == '#':
                    fixedArgs.append([])
                else:
                    # need to replace extra quotes for paths with spaces
                    theList = map(lambda a: cast(a.replace('"','').replace("'","")), arg.split(';'))
                    if theList == ['']:
                        theList = []
                    fixedArgs.append(theList)
            else:
                if arg_type.lower() in stringTypes:
                    fixedArgs.append([str(a) for a in arg])
                else:
                    fixedArgs.append(arg)

        # string other types
        elif arg_type.lower() in stringTypes:
            if arg in [None, '', '#']:
                fixedArgs.append('')
            else:
               fixedArgs.append(str(arg))

        # append raw value as object
        else:
            isLyrOrTab = False
            if arg_type.lower() in ('table view', 'feature layer'):
                #fixedArgs.append(arcpy.Describe(arg).catalogPath)
                fixedArgs.append(arg)
                isLyrOrTab = True

            if not isLyrOrTab:
                fixedArgs.append(arg)
    return fixedArgs

def parseValueTable(vt, frmat='dict', value_type=None):
    """parses a value table to either a dictionary or nested list

    Required:
        vt -- value table as string

    Optional:
        frmat -- return format. Default is 'dict'.  Use
            'list' to return as nested list.
    """
    if frmat == 'dict':
        d = OrderedDict()
    else:
        d = []
    for row in vt.split(';'):
        if "'" in row:
            all_vals = filter(None, row.split("'"))
            if len(all_vals) > 2:
                key, value = all_vals[0], [v for v in all_vals[1:] if v != ' ']
            elif len(all_vals) == 2:
                key, value = all_vals[0], all_vals[1].split()
            if len(value) == 1 and isinstance(value, list):
                value = value[0]
        else:
            if row.count(' ') > 1:
                rowVals = row.split()
                key = rowVals[0]
                value = rowVals[1:]
            else:
                key, value = row.split()

        if isinstance(value, list):
            value = [v.strip() for v in value]
        else:
            value = value.strip()

        # cast value types
        if value_type not in (None, '', ' ', '#'):
            if isinstance(value, list):
                value = map(value_type, value)
            else:
                value = value_type(value)

        # add to list or dictionary
        if frmat == 'dict':
            d[key.strip()] = value
        else:
            d.append([key.strip(), value])
    return d

def ErrorLog(e, f, fargs=[]):
    """generate an error log when tool fails"""

    # Get the traceback object
    date = time.strftime('%m_%d_%Y')
    cur = os.path.basename(sys.argv[0]).split('.')[0]
    er_time = '\n\n{0} failed at:\t{1}\n\n'.format(cur, datetime.datetime.now())
    log_dir = os.path.join(os.path.dirname(SOURCE_DIR), 'logs', 'errors')


    txt = os.path.join(log_dir, 'ERROR_{0}_{1}.txt'.format(cur, date))
    if os.path.exists(txt):
        try:
            os.remove(txt)
        except:
            pass
    logging.basicConfig(filename=txt, level=logging.DEBUG)
    user_info = '\n\n'.join(['\n\nUser: {0}'.format(os.environ['USERNAME']), 'Inputs:', '\t' + str(fargs)])
    user_info += '\n\nScript:\t{}\n\n'.format(sys.argv[0])

    logger = logging.getLogger(f.__module__)
    logging.debug(''.join([er_time, user_info]))
    logger.exception(e)
    del logger

    # raise full message
    with open(txt, 'rt') as fl:
        body = fl.read()
    raise Exception(body)

def toolLog(f, test=False):
    """Adds log of tool usage [tool, user, date, time, am-pm]"""
    if hasattr(f, 'im_class'):
        tool = '.'.join(filter(lambda x: isinstance(x, basestring), [f.__module__, f.im_class.__name__, f.__name__]))
    else:
        tool = '.'.join([f.__module__, f.__name__])
    date = time.strftime('%Y-%m-%d')
    curtime = time.strftime('%I:%M:%S %p')
    usr = os.environ['USERNAME']
    report = '\t'.join([tool,usr,date,curtime])

    # Append to appropriate text file
    path = os.path.join(os.path.dirname(SOURCE_DIR), 'logs', 'logs')

    # New text file for every month
    txt = os.path.join(path, time.strftime('%Y_%m_%b.txt'))
    with open(txt, 'a') as f:
        f.write(report + '\n')
    return report

def timeit(function):
    """will time a function's execution time

    Required:
    function -- full namespace for a function

    Optional:
    args -- list of arguments for function
    """
##    if function.__name__ != 'writeConfig':
##        toolLog(function)
    st = datetime.datetime.now()
    def wrapper(*args, **kwargs):
        output = function(*args, **kwargs)
        if hasattr(function, 'im_class'):
            fname = '.'.join([function.im_class.__name__, function.__name__])
        else:
            fname = function.__name__
        Message('"{0}" from {1} Complete - Elapsed time: {2}'.format(fname, sys.modules[function.__module__],
                                                            str(datetime.datetime.now()-st)[:-4]))
        return output
    return wrapper

def passArgs(function, argv=[]):
    '''
    passes arguments to a function from script tool.

    function: name of function
    argv: arguments for function from script tool
    '''
    toolLog(function)
    f = None
    if not argv:
        argv = fixGpArgs()

    try:
        if isinstance(argv, dict):
            f = function(**argv)
        else:
            f = function(*argv)
    except Exception as e:
       ErrorLog(e, function, argv)

##    if f:
##        Message('{}.{}() Result:\n{}\ntype: {}'.format(function.__module__, function.__name__, f, type(f)))
    return f

#***********************************************************************************************************
#
# Little River Drainage District utilities
def zipdir(path, out_zip=''):
    """zips a folder and all subfolders

    Required:
        path -- folder to zip

    Optional:
        out_zip -- output zip folder. Default is path + '.zip'
    """
    rootDIR = os.path.basename(path)
    if not out_zip:
        out_zip = path + '.zip'
    else:
        if not out_zip.strip().endswith('.zip'):
            out_zip = os.path.splitext(out_zip)[0] + '.zip'
    zipFile = zipfile.ZipFile(path + '.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for fl in files:
            if not fl.endswith('.lock'):
                subfolder = os.path.basename(root)
                if subfolder == rootDIR:
                    subfolder = ''
                zipFile.write(os.path.join(root, fl), os.path.join(subfolder, fl))
    return out_zip

def unzip(z, new=''):
    """unzip a zipped file

    Optional:
        new -- output folder, if not specified will default to same directory as zip
        folder.
    """
    if not new:
        new = os.path.splitext(z)[0]
    with zipfile.ZipFile(z, 'r') as f:
        f.extractall(new)
    return

def find_ws(path, ws_type='', return_type=False):
    """finds a valid workspace path for an arcpy.da.Editor() Session

    Required:
        path -- path to features or workspace

    Optional:
        ws_type -- option to find specific workspace type (FileSystem|LocalDatabase|RemoteDatabase)
        return_type -- option to return workspace type as well.  If this option is selected, a tuple
            of the full workspace path and type are returned

    """
    def find_existing(path):
        if arcpy.Exists(path):
            return path
        else:
            if not arcpy.Exists(path):
                return find_existing(os.path.dirname(path))

    # try original path first
    if isinstance(path, (arcpy.mapping.Layer, arcpy.mapping.TableView)):
        path = path.dataSource
    if os.sep not in str(path):
        if hasattr(path, 'dataSource'):
            path = path.dataSource
        else:
            path = arcpy.Describe(path).catalogPath

    path = find_existing(path)
    desc = arcpy.Describe(path)
    if hasattr(desc, 'workspaceType'):
        if ws_type == desc.workspaceType:
            if return_type:
                return (path, desc.workspaceType)
            else:
                return path
        else:
            if return_type:
                return (path, desc.workspaceType)
            else:
                return path

    # search until finding a valid workspace
    path = str(path)
    SPLIT = filter(None, str(path).split(os.sep))
    if path.startswith('\\\\'):
        SPLIT[0] = r'\\{0}'.format(SPLIT[0])

    # find valid workspace
    for i in xrange(1, len(SPLIT)):
        sub_dir = os.sep.join(SPLIT[:-i])
        desc = arcpy.Describe(sub_dir)
        if hasattr(desc, 'workspaceType'):
            if ws_type == desc.workspaceType:
                if return_type:
                    return (sub_dir, desc.workspaceType)
                else:
                    return sub_dir
            else:
                if return_type:
                    return (sub_dir, desc.workspaceType)
                else:
                    return sub_dir


def assignUniqueName(fl):
    """assigns a unique file name
    Required:
        fl -- file name
    """
    if not os.path.exists(fl):
        return fl

    i = 1
    head, tail = os.path.splitext(fl)
    new_name = '{}_{}{}'.format(head, i, tail)
    while os.path.exists(new_name):
        i += 1
        new_name = '{}_{}{}'.format(head, i, tail)
    return new_name

#**********************************************************************************************************
#
# Little River Drainage District Utilities
def getConfig():
    """get configuration file back as Munch"""
    if not os.path.exists(CONFIG):
        raise IOError('Configuration File "{}" does not exist!'.format(CONFIG))
    return munch.munchify(json.load(open(CONFIG, 'r'), 'utf-8'))

def getParcelConfig(configFile):
    """get parcel field configuration"""
    if not os.path.exists(configFile):
        raise IOError('Configuration file does not exist!\nThis file must be set up before running tools.')
    with open(configFile, 'r') as f:
        return munch.munchify(json.load(f))

def getParcelFields():
    """get parcel configuration fields as bunch"""
    if not os.path.exists(PARCEL_FIELDS):
        # got deleted somehow, grab from zipped folder
        source = os.path.join(BIN, 'data', os.path.basename(PARCEL_FIELDS).split('.')[0] + '.zip')
        unzip(source, BIN)

    with open(PARCEL_FIELDS, 'r') as f:
        return munch.munchify(json.load(f)['fields'])

def getParcelLRFields():
    """get parcel configuration fields as bunch"""
    if not os.path.exists(PARCEL_LR_FIELDS):
        # got deleted somehow, grab from zipped folder
        source = os.path.join(BIN, 'data', os.path.basename(PARCEL_LR_FIELDS).split('.')[0] + '.zip')
        unzip(source, BIN)

    with open(PARCEL_LR_FIELDS, 'r') as f:
        return munch.munchify(json.load(f)['fields'])

def getFieldMapDict(configFile):
    """gets the field map dictionary"""
    conf = getParcelConfig(configFile)
    return {v:k for k,v in conf.field_map.iteritems()}

def getTemplate():
    """get template fields"""
    if not os.path.exists(TEMPLATE):
        # got deleted somehow, grab from zipped folder
        source = os.path.join(BIN, 'data', 'template.zip')
        unzip(source, BIN)

    with open(TEMPLATE, 'r') as f:
        return munch.munchify(json.load(f))

def writeConfig(**kwargs):
    """write configuration file to JSON"""
    d = {k:v for k,v in kwargs.iteritems()}
    with open(CONFIG, 'w') as f:
        json.dump(d, f, indent=4, sort_keys=True, ensure_ascii=False)

def fieldMappings(fcs_in, dico):
    """matches fields for field mapping

    Required:
        fcs_in -- list of feature classes to apply field mappings
        dico -- field mappings dictionary {other_name: target_name}

    # Dictionary key: field to be mapped from other fc
    # Dictionary value: output target field name
    """

    field_mappings = arcpy.FieldMappings()
    if isinstance(fcs_in, basestring):
        fcs_in = fcs_in.split(';')
    for fc_in in fcs_in:
        field_mappings.addTable(fc_in)

    for inputF, output in dico.iteritems():
        if inputF != '<None>' and output != '<None>':
            field_map = arcpy.FieldMap()
            try:
                in_field = field_map.addInputField(fc_in, inputF)
                field = field_map.outputField
                field.name = output
                field_map.outputField = field
                field_mappings.addFieldMap(field_map)
                print 'Changing input field "{}" to output field "{}"'.format(inputF, output)
                del field, field_map
            except:
                print "Could not add '{0}' field to \"{1}\"".format(inputF,fc_in)

    return field_mappings

def hasValue(in_data):
    """make sure value is valid"""
    if in_data in (None, '') or str(in_data).strip() == '':
        return False
    return True

def sortkeypicker(keynames):
    """sort dict by multiple keys, from the great Alex Martelli

    keynames -- list of keys to sort by

    http://stackoverflow.com/questions/1143671/python-sorting-list-of-dictionaries-by-multiple-keys
    """
    if isinstance(keynames, basestring):
        keynames = keynames.split(',')
    negate = set()
    for i, k in enumerate(keynames):
        if k[:1] == '-':
            keynames[i] = k[1:]
            negate.add(k[1:])
    def getit(adict):
       composite = [adict[k] for k in keynames]
       for i, (k, v) in enumerate(zip(keynames, composite)):
           if k in negate:
               composite[i] = -v
       return composite
    return getit

def getPIN(in_pid):
    """returns PIN with numbers only"""
    if in_pid is None:
        return ''
    return in_pid.replace('.', '').replace('-','').replace(' ','')

class Geodatabase(object):
    """Wrapper for Little River District Geodatabase

    Properties:
        summary_table -- contains the summary assessments for each parcel, should match up with
            each county's ParcelsLR feature class.  This table is used for the Abstract of Receipts.

        maintenance_table -- contains the summary assessment breakdowns for each parcel and represents
            the subdivision of any parcels that are broken into <= 40 acre tracts.  This is used for
            the tax book/maintenance assessment list.

        active_owners -- table for active owners.  This is the master table for address information
            for the district.  Edits to address info should happen here.

        llrd_fields -- list of fields used in getting Owner and Landowner objects, this info is mined
            from the summary_table and combined with info from the parcels tables.

        parsLR_fields -- list of fields from ParcelsLR feautre class pertinent to the little river
            district tax process.

        aoc_fields -- list of fields from the Active Owner Codes table

        aoc_keys -- keys for the the Owner object individual assessment dictionaries

        current_ws -- current arcpy.env.workspace, typically is the path of this geodatabase

        path -- full path to this geodatabase

        district -- full path to the Little River District Boundary
    """
    par_summary_table_name = 'Parcel_Assessment_Summary'
    par_breakdown_table_name = 'Parcel_Assessment_Breakdown'
    flag_table_name = 'Breakdown_Flags'

    # fields
    aoc_fields = ['LO_ID', 'LO_NAME', 'LO_NAME2', 'LO_ADDR1', 'LO_ADDR2', 'LO_CITY',
                  'LO_ST', 'LO_ZIP', 'LO_ACTIVE']

    llrd_fields = ['OWNER_CODE', PARCEL_ID, 'DATE_PAID', 'ASSESSED_ACRES', 'TOT_BENEFIT',
                   'TOT_ASSESSMENT', 'TOT_ADMIN_FEE', 'PENALTY', 'EXCESS', 'AMOUNT_PAID']

    parsLR_fields = ['OWNER_CODE', PARCEL_ID, 'LEG_DESC1', 'LEG_DESC2', 'SECTION', 'ACRES',
                    'GIS_ACRES', 'TOWNSHIP', 'RANGE', 'ADDRESS1', 'ADDRESS2', 'CITY', 'STATE', 'ZIP', PIN]

    breakdown_fields = ['CODE', 'LANDOWNER_NAME', 'SECTION', 'TOWNSHIP', 'RANGE', 'SEQUENCE', 'DESCRIPTION',
                        'COUNTY_MAP_NUMBER', 'ACRES', 'BENEFIT', 'ASSESSMENT', 'EXEMPT', 'DATE_PAID', 'COUNTY',
                        'FLAG', 'PIN', 'SEC_TWN_RNG']


    aoc_keys = ['code', 'name', 'name2', 'address', 'address2', 'city', 'state', 'zip', 'isActive']

    def __init__(self):
        """initialize to refresh path in case it changes"""
        self.path = getConfig().Geodatabase
        self.district = os.path.join(self.path, 'Misc_Dataset', 'LittleRiver_2016DistrictBnds')
        self.active_owners = os.path.join(self.path, 'Active_Owner_Codes')
        self.summary_table = os.path.join(self.path, self.par_summary_table_name)
        self.breakdown_table = os.path.join(self.path, self.par_breakdown_table_name)
        self.flag_table = os.path.join(self.path, self.flag_table_name)
        self.current_ws = self.path
        arcpy.env.workspace = self.path

    def walk(self, wild='*', ftype='All'):
        """
        Returns a generator for all feature classes in the geodatabase.

        Optional:
            wild -- wildcard for feature classes
            ftype -- feature class type (point, line, polygons, etc)
        """
        # feature type (add all in case '' is returned
        # from script tool
        arcpy.env.workspace = self.path
        self.current_ws = self.path
        if not ftype:
            ftype = 'All'

        # Add top level fc's (not in feature data sets)
        for fc in arcpy.ListFeatureClasses(wild, ftype):
            yield os.path.join(self.path, fc)

        # loop through feature datasets
        for fd in arcpy.ListDatasets('*', 'Feature'):
            arcpy.env.workspace = fdws = os.path.join(self.path, fd)
            for fc in arcpy.ListFeatureClasses(wild, ftype):
                yield os.path.join(fdws, fc)

    @staticmethod
    def getCounty(county):
        """validates a county input"""
        county = ' '.join(county.split())
        if not 'COUNTY' in county.upper():
            county += ' COUNTY'

        return county.upper()

    @staticmethod
    def list_counties(wsName=False):
        """get list of counties, if wsName is set to True, it will return the names
        matching the feature datasets
        """
        counties = ['Bollinger County', 'Cape Girardeau County', 'Dunklin County', 'New Madrid County',
                    'Pemiscot County', 'Scott County', 'Stoddard County']
        if wsName:
            return [c.replace(' ','_') for c in counties]
        return counties

    def iterParcels(self, ptype='lr'):
        """iterates all parcels of either lr or county type

        """
        if ptype.lower() == 'lr':
            wildcard = '*_ParcelsLR'
        else:
            wildcard = '*_Parcels'

        for fc in self.walk(wildcard):
            yield fc

    def getOwnerCodes(self):
        """gets a list of owner codes"""
        with arcpy.da.SearchCursor(self.breakdown_table, ['CODE']) as rows:
           return sorted(list(set(r[0] for r in rows if r[0])))

    def getParcelPath(self, name, pType='lr'):
        """retrieve full path to parcel data set by county name

        Required:
            name -- name of county

        Optional:
            pType -- type of parcels, default is lr (lr|county)
        """
        name = '_'.join(name.title().split())
        if not name.endswith('_County'):
            name += '_County'

        arcpy.env.workspace = fds = os.path.join(self.path, name)
        self.current_ws = fds
        if pType.lower() == 'lr':
            wild = '*_ParcelsLR'
        else:
            wild = '*_Parcels'

        feats = os.path.join(fds, arcpy.ListFeatureClasses(wild)[0])
        arcpy.env.workspace = self.path
        self.current_ws = self.path
        return feats

    def getParcelSummaryDict(self):
        """returns the parcel summary table dict, with the key being the PIN"""
        fields = ['OWNER_CODE', 'TOT_ASSESSMENT', 'DATE_PAID', 'TOT_BENEFIT', 'TOT_ADMIN_FEE']
        with arcpy.da.SearchCursor(self.summary_table, [PIN] + fields) as rows:
            return {r[0]: r[1:] for r in rows}

    def updateParcels(self, parcels, county, field_map):
        """replace parcels with new parcels downloaded from FTP site

        Required:
            parcels -- input parcels to replace existing parcels
            county -- name of county to update in Geodatabase
            field_map -- dictionary for field mappings where the keys are the county parcels'
                fields and values that match the Little River DD GDB schema
        """
        pars = self.getParcelPath(county, 'county')
        if isinstance(field_map, arcpy.FieldMappings):
            fmap = field_map

        elif isinstance(field_map, dict):
            if field_map.keys()[0] in [f.name for f in getParcelFields()]:
                # we need to reverse the dict
                field_map = {v:k for k,v in field_map.iteritems()}
            fmap = fieldMappings([pars, parcels], field_map)

        # delete rows first, then append
        arcpy.management.DeleteRows(pars)
        arcpy.management.Append(parcels, pars, 'NO_TEST', fmap)

        # validate Section Township Range and calc acres
        plss = pars.replace('_Parcels', '_PLSS')
        spa_join = r'in_memory\tmp_spa_join'

        # spatial join
        arcpy.analysis.SpatialJoin(pars, plss, spa_join)
        with arcpy.da.SearchCursor(spa_join, ['TARGET_FID', 'TWN', 'SEC', 'RNG']) as rows:
            for r in rows:
                secs = {r[0]: r[1:] for r in rows}

        # now update in parcels table
        existing_fields = [f.name for f in arcpy.ListFields(pars)]
        if PIN not in existing_fields:
            arcpy.management.AddField(pars, PIN, 'TEXT')

        if SEC_TWN_RNG not in existing_fields:
            arcpy.management.AddField(pars, SEC_TWN_RNG, 'TEXT', field_alias='SEC-TWN-RNG')

        with UpdateCursor(pars, ['OID@', 'TOWNSHIP', 'SECTION', 'RANGE', PARCEL_ID, PIN, SEC_TWN_RNG]) as rows:
            for r in rows:
                if r[0] in secs:
                    r[1:4] = ['{:0>2}'.format(p) if p else '99' for p in secs[r[0]] ]
                    r[5] = r[4].replace('.','').replace('-','').strip()
                    r[6] = '-'.join(r[1:4])
                    rows.updateRow(r)

        # now do LR parcels
        lr_pars = pars + 'LR'
        if arcpy.Exists(lr_pars):
            arcpy.management.Delete(lr_pars)

        # clip parcels to district in memory
        pars_clip = r'in_memory\tmp_pars'
        arcpy.analysis.Clip(pars, self.district, pars_clip)

        # dissolve, too many duplicated/multi-part parcels
        dis_fields = [f.name for f in getParcelFields()] #+ ['Shape_Area']
        arcpy.management.Dissolve(pars_clip, lr_pars, dis_fields)

        # get lr extra fields and add them
        target_fields = ['GIS_ACRES', 'OWNER_CODE', 'TOT_ASSESSMENT', 'DATE_PAID', 'TOT_BENEFIT', 'TOT_ADMIN_FEE']
        lr_fields = getParcelLRFields()
        for fld in lr_fields:
            if fld.name in target_fields:
                arcpy.management.AddField(lr_pars, fld.name, fld.type, field_alias=fld.alias, field_length=fld.length)

        # get summary dict
        sumd = self.getParcelSummaryDict()

        # calculate acres and LR fields
        with UpdateCursor(lr_pars, ['SHAPE@'] + target_fields + [PIN]) as rows:
            for r in rows:
                r[1] = r[0].area / 43560.0 # not going to use getArea here in case they are not  on v 10.2+

                if r[-1] in sumd:
                    r[2:-1] = sumd[r[-1]]

                rows.updateRow(r)

        Message('Successfully updated parcels for: "{}"'.format(county))
        return lr_pars

    def getOwners(self, county):
        """Generates LandOwners object for a county

        Required:
            county - county name for which to get all landowners
        """
        # get unique list of landowners within county and form where clause from *_ParcelsLR
        parsLR = self.getParcelPath(county)
        par_dict = {}
        owner_ids = []
        with arcpy.da.SearchCursor(parsLR, self.parsLR_fields) as rows:
            for r in rows:
                if hasValue(r[0]):
                    owner_ids.append(r[0])
                    par_dict[r[1]] = dict(zip([f.lower() for f in self.parsLR_fields[2:]], r[2:]))

        # form where clause to select only owner codes found within county
        codes = tuple(str(c) for c in set(owner_ids))
        where_aoc = 'LO_ID in {}'.format(codes)
        where_lrdd = 'OWNER_CODE in {}'.format(codes)

        # grab info from  AOC table
        with arcpy.da.SearchCursor(self.active_owners, self.aoc_fields, where_clause=where_aoc) as rows:
            aoc = [dict(zip(self.aoc_keys, r)) for r in rows]

        # get assessments
        dd_dict = {k['code']: [] for k in aoc}
        with arcpy.da.SearchCursor(self.summary_table, self.llrd_fields, where_clause=where_lrdd) as rows:
            for r in rows:
                if r[0] in dd_dict:
                    dd_dict[r[0]].append(dict(zip([f.lower() for f in self.llrd_fields][1:], r[1:])))

        # add assements to to aoc json
        for owner in aoc:

            if owner['code'] in dd_dict:

                # create assessments list
                owner['assessments'] = []
                parLR_atts = dd_dict[owner['code']]

                # add each parcel to be assessed
                for parLR in parLR_atts:

                    pin = parLR['parcel_id']

                    # make a copy
                    parLR_copy = {k:v for k,v in parLR.iteritems()}

                    if pin in par_dict:

                        # combine with *_ParcelsLR attributes
                        for key, value in par_dict[pin].iteritems():
                            if key in ('sec', 'twn', 'rng'):
                                parLR_copy[key] = '{:0>2}'.format(value)
                            else:
                                parLR_copy[key] = value

                        # add address info from parcels if it does not already exist
                        if not hasValue(owner['city']) and hasValue(parLR_copy['city']):
                            owner['city'] = parLR_copy['city']

                        if not hasValue(owner['state'])  and hasValue(parLR_copy['state']):
                            owner['state'] = parLR_copy['state']

                        if not hasValue(parLR_copy['zip'])  and hasValue(parLR_copy['zip']):
                            owner['zip'] = parLR_copy['zip']

                        if not hasValue(owner['address'])  and hasValue(parLR_copy['address1']):
                            owner['address'] = parLR_copy['address1']

                        if all(map(hasValue, [owner['city'], owner['state'], owner['zip']])):
                            owner['address_suffix'] = '{}, {} {}'.format(*[owner['city'], owner['state'], owner['zip']])

                        else:
                            # add address2 field from parcels
                            owner['address_suffix'] = parLR_copy['address2']

                        #*************************************************************************************************
                        # Little River District Database has extra parcel IDs not found in county parcel dataset
                        # move this back outside the if statement if want to include all

                    # add to assessments
                    owner['assessments'].append(parLR_copy)

        try:
            county_pretty = [c for c in self.list_counties() if fnmatch.fnmatch(c, '{}*'.format(county))][0]
        except IndexError:
            county_pretty = county

        # return LandOwners() object
        return LandOwners(county_pretty, munch.munchify(aoc))

    def getOwnerReceiptDict(self, county='', year=LAST_YEAR, where_clause=''):
        """generates owner receipt dict

            {
              "code": "DRUI01",
              "name": "DRURY INDUSTRIES INC",
              "address": "101 S FARRAR DRIVE",
              "csz": "CAPE GIRARDEAU MO 6371",
              "county": "CAPE GIRARDEAU COUNTY",
              "year": 2015,
              "assessments": [
                {
                  "SN-TP-RG": "27-30-13",
                  "SEQ": "0170",
                  "DESCRIPTION & MAP NUMBER": "PT S1/2 NE\r\n20-802-27-00-1300-0000",
                  "ACRES": 3.5,
                  "BENEFITS": 88.00,
                  "DRAINAGE FEE AMOUNT": 7.92,
                  "pin": "20-802-27-00-1300-0000"
                },
                {
                  "SN-TP-RG": "99-99-99",
                  "SEQ": "99999",
                  "DESCRIPTION & MAP NUMBER": "ADMINISTRATIVE FEE\r\n20-802-27-00-1300-0000",
                  "ACRES": 0,
                  "BENEFITS": 0,
                  "DRAINAGE FEE AMOUNT": 19.58,
                  "pin": "20-802-27-00-1300-0000"
                }
              ]
            }

        """
        # build initial owner dict
        if county:
            county = self.getCounty(county)
            county_where = "COUNTY = '{}'".format(county)
        else:
            county_where = ''
        where = 'AND '.join(filter(lambda w: w not in ('', None, '#'), [county_where, where_clause]))
        own_root_fields = ['CODE', 'LANDOWNER_NAME', 'COUNTY']
        with arcpy.da.SearchCursor(self.breakdown_table, own_root_fields, where) as rows:
            owners = {r[0]: {'code': r[0],
                             'name': r[1],
                             'address': '',
                             'csz': '',
                             'year': year,
                             'county': r[2],
                             'assessments': []}
                    for r in rows if r}

        # get address info
        addr_fields = ['LO_ID', 'LO_ADDR1', 'LO_ADDR2', 'LO_CITY', 'LO_ST', 'LO_ZIP']
        with arcpy.da.SearchCursor(self.active_owners, addr_fields, county_where) as rows:
            for r in rows:
                if r[0] in owners:
                    owners[r[0]]['address'] = ' '.join(filter(None, r[1:3]))

                    # attempt to nicely format city, state zip
                    if len(filter(None, r[3:])) == 3:
                        owners[r[0]]['csz'] = '{}, {} {}'.format(*r[3:])
                    else:
                        owners[r[0]]['csz'] = ' '.join([s if s else '' for s in r[3:]])

        # loop back through original table to get assessments
        assess_flds = ['COUNTY_MAP_NUMBER', 'ACRES', 'BENEFIT', 'ASSESSMENT',
                       'SEC_TWN_RNG', 'SEQUENCE', 'DESCRIPTION', 'CODE']

        match_flds = ['pin', 'ACRES', 'BENEFITS', 'DRAINAGE FEE AMOUNT', 'SN-TP-RG', 'SEQ']

        with arcpy.da.SearchCursor(self.breakdown_table, assess_flds, where) as rows:
            for r in rows:
                if r[-1] in owners:
                    ad = dict(zip(match_flds, r[:-2]))
                    ad['DESCRIPTION & MAP NUMBER'] = '\r\n'.join([s if s else '' for s in [r[-2], r[0]]])
                    owners[r[-1]]['assessments'].append(ad)

        return munch.munchify(owners)


class Owner(object):
    """class to handle owner info"""
    json = {}
    sortBy = 'code'
    def __init__(self, in_json, sortBy='code'):
        """instantiate owner object

        Required:
            in_json -- input dictionary representing owner info

        pretty print representation:
          {
              "city": "CHAFFEE",
              "address_suffix": "CHAFFEE, MO 63740",
              "code": "ABEE01",
              "name": "ABERNATHY ELVIS & JUDITH",
              "zip": "63740",
              "address2": null,
              "state": "MO",
              "name2": null,
              "address": "ROUTE 2 BOX 124",
              "assessments": [
                {
                  "admin_fee": 24.799999237060547,
                  "zip": null,
                  "city": null,
                  "assessed_acres": 0.8209729790687561,
                  "address1": "768 HELEN AVE",
                  "address2": null,
                  "parcel_id": "043.007.00000000004.30",
                  "gis_acres": 0.8209778250053811,
                  "acres": 0.8209729790687561,
                  "penalty": null,
                  "date_paid": null,
                  "state": null,
                  "amount_paid": null,
                  "benefit": 30.0,
                  "excess": null,
                  "range": "13",
                  "township": "29",
                  "assessment": 2.700000047683716,
                  "section": "7",
                  "leg_desc1": "PT W PT LOT 2 SW1/4 E OF HWY 77 &",
                  "leg_desc2": "N OF HELEN ST JCT CHAFFEE"
                }
              ],
              "isActive": "TRUE"
            }

        """
        self.json = munch.munchify(in_json)
        self.sortBy = sortBy
        for k,v in self.json.iteritems():
            setattr(self, k, v)

    @property
    def pins(self):
        """return a list of all unique Parcel ID's"""
        return sorted(list(set([p.parcel_id for p in iter(self)])))

    @property
    def active(self):
        """turns string into boolean"""
        return self.isActive == 'TRUE'

    @property
    def parcelCount(self):
        """return count of parcels, differnt from number of assessments.  Will count
        number of unique parcels"""
        return len(self.pins)

    @staticmethod
    def plss(owner_json):
        """return formatted sec-twn-rng string from Owner.json object"""
        atts = filter(None, [owner_json.sec, owner_json.twn, owner_json.rng])
        if len(atts) == 3:
            return '-'.join(map(lambda s: str(s).zfill(2), atts))
        return ''

    @staticmethod
    def getYear(owner_json):
        """return year from owner_json object"""
        date = owner_json.date_paid
        if isinstance(date, datetime.datetime):
            return date.year
        return date

    def sum(self, attr):
        """summarizes attributes from all assessments

        Required:
            attribute to summarize based on, must be one of these values:

        (benefit|assessment|admin_fee|tax_paid|collection|assessed_acres|gis_acres|)
        """
        valid = ['benefit', 'assessment', 'admin_fee', 'tax_paid',
                 'collection', 'assessed_acres', 'gis_acres']
        if attr.lower() not in valid:
            return 0
        try:
            return sum(parcel.get(attr.lower(), 0) for parcel in iter(self))
        except KeyError:
            return 'N/A'

    def __repr__(self):
        """pretty print"""
        return json.dumps(self.json, indent=2)

    def __getitem__(self, name):
        """dict like access to json definition or assessment index"""
        if isinstance(name, int):
            return self.json['assessments'][name]

        elif name in self.json:
            return self.json[name]

    def __iter__(self):
        """generator for all parcels for Owner"""
        for parcel in self.json.assessments:
            yield parcel

    def __len__(self):
        """count of parcel assessments"""
        return len(self.json.assessments)

    def __nonzero__(self):
        """is not 0"""
        return bool(len(self))

    def __eq__(self, other):
        """test for equality"""
        if isinstance(other, self.__class__):
            return self.json == other.json
        return False

class LandOwners(object):
    """class to handle landowners for a county"""
    def __init__(self, county, owners=[], sortBy='code'):
        self.county = county
        self.owners = [Owner(o) for o in sorted(owners, key=sortkeypicker(sortBy))]
        self.count = len(self)
        self.parcelCount = sum(len(o) for o in self.owners)
        self._sortBy = sortBy

    @property
    def sortBy(self):
        """sortBy property"""
        return self._sortBy

    @sortBy.setter
    def sortBy(self, key):
        """setter to change sortBy attribute, when this is changed the owners will
        be re-sorted.

        Required:
            key -- key to sort owners by (from Geodatabase.aoc_keys)
        """
        self.sort(key)

    def sort(self, sortBy=None, reverse=False):
        """sort owners by a key

        Required:
            sortBy -- name of key to sort owners by (from Geodatabase.aoc_keys)

        Optional:
            reverse -- option to sort by Descending order.  False by default.
        """
        if sortBy is None or sortBy.lower() not in Geodatabase.aoc_keys:
            sortBy = self._sortBy

        if sortBy.lower() in Geodatabase.aoc_keys:
            self._sortBy = sortBy.lower()

            self.owners = sorted(self.owners, key=sortkeypicker(sortBy), reverse=reverse)

    def find(self, code):
        """find owner by code"""
        for owner in iter(self):
            if owner.code == code:
                return owner

    def findByPID(self, pid):
        """find owner by parcel ID"""
        for owner in iter(self):
            if str(pid) in owner.pins:
                return owner

    def findByName(self, name):
        """find owner by name"""
        for owner in iter(self):
            if owner.name == name:
                return owner

    def findOwners(self, **kwargs):
        """performs a wildcard search based on kwargs"""
        for k,v in kwargs.iteritems():
            if k in Geodatabase.aoc_keys:
                attr, wildcard = k,v
                break # only allow for one kwarg
        matches = []
        if kwargs:
            for owner in self.owners:
                if fnmatch.fnmatch(getattr(owner, attr), v):
                    matches.append(owner)

        return matches

    def __iter__(self):
        """generator for owners"""
        for owner in self.owners:
            yield owner

    def __getitem__(self, index):
        """get assessment by index"""
        return self.owners[index]

    def __len__(self):
        """count of owners in county"""
        return len(self.owners)

    def __nonzero__(self):
        """is not 0"""
        return bool(len(self))

    def __repr__(self):
        return '<Landowners "{}">'.format(self.county)


class UpdateCursor(object):
    """wrapper clas for arcpy.da.UpdateCursor, to automatically
    implement editing (required for versioned data, and data with
    geometric networks, topologies, network datasets, and relationship
    classes"""
    def __init__(self, *args, **kwargs):
        """initiate wrapper class for update cursor.  Supported args:

        in_table, field_names, where_clause=None, spatial_reference=None,
        explode_to_points=False, sql_clause=(None, None)
        """
        self.args = args
        self.kwargs = kwargs
        self.edit = None

    def __enter__(self):
        ws = None
        if self.args:
            ws = find_ws(self.args[0])
        elif 'in_table' in self.kwargs:
            ws = find_ws(self.kwargs['in_table'])

        self.edit = arcpy.da.Editor(ws)
        self.edit.startEditing()
        self.edit.startOperation()
        return arcpy.da.UpdateCursor(*self.args, **self.kwargs)

    def __exit__(self, type, value, traceback):
        self.edit.stopOperation()
        self.edit.stopEditing(True)
        self.edit = None

class InsertCursor(object):
    """wrapper clas for arcpy.da.InsertCursor, to automatically
    implement editing (required for versioned data, and data with
    geometric networks, topologies, network datasets, and relationship
    classes"""
    def __init__(self, *args, **kwargs):
        """initiate wrapper class for update cursor.  Supported args:

        in_table, field_names
        """
        self.args = args
        self.kwargs = kwargs
        self.edit = None

    def __enter__(self):
        ws = None
        if self.args:
            ws =  find_ws(self.args[0])
        elif 'in_table' in self.kwargs:
            ws =  find_ws(self.kwargs['in_table'])
        self.edit = arcpy.da.Editor(ws)
        self.edit.startEditing()
        self.edit.startOperation()
        return arcpy.da.InsertCursor(*self.args, **self.kwargs)

    def __exit__(self, type, value, traceback):
        self.edit.stopOperation()
        self.edit.stopEditing(True)
        self.edit = None