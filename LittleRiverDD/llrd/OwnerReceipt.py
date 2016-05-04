#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     18/04/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from . import excel
import xlwt
reload(excel)
from excel import *
from excel_styles import *
from . import utils
from .mailing import avery5160
import os
import arcpy
import sys
import json
from string import ascii_uppercase

arcpy.env.overwriteOutput = True

# third party
SOURCE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(SOURCE_DIR, 'thirdParty'))
import munch

# headers
YEAR = 'YEAR'
SECTION = 'SN-TP-RG'
SEQUENCE = 'SEQ'
DESCRIPTION = 'DESCRIPTION & MAP NUMBER'
ACRES = 'ACRES'
BENEFITS = 'BENEFITS'
DRAINAGE_FEE = 'DRAINAGE FEE AMOUNT'
BLANK = ' '

# fields from breakdown table
CODE_GIS = 'CODE'
SEC_TWN_RNG_GIS = 'SEC_TWN_RNG'
LANDOWNER_GIS = 'LANDOWNER_NAME'
DESCRIPTION_GIS = 'DESCRIPTION'
PID_GIS = 'COUNTY_MAP_NUMBER'
ACRES_GIS = 'ACRES'
BENEFIT_GIS = 'BENEFIT'
ASSESSMENT_GIS = 'ASSESSMENT'
EXEMPT_GIS = 'EXEMPT'
SEQUENCE_GIS = 'SEQUENCE'
DATE_PAID_GIS = 'DATE_PAID'
COUNTY_GIS = 'COUNTY'

# Fields from parcels LR feature classess
PARCEL_ID_LR = 'PARCEL_ID'

# Label Expression for selected parcels
LABEL_EXPRESSION = '''"<CLR red='255' green='255'><FNT size='9'>" & [{}] & "</FNT></CLR>"'''.format(PARCEL_ID_LR)

# constants
DEFAULT_MAIL_NAME = 'DIANE DIEBOLD'
DEFAULT_MAIL_ADDR = '1 BARTON SQUARE'
DEFAULT_MAIL_CSZ = 'JACKSON, MO 63755'
PENALTY = '(PENALTY OF 1% PER MONTH ATTACHES AFTER JANUARY FIRST) = TOTAL PENALTY AMOUNT ---------------->'
TOT_PEN = 'TOTAL DRAINAGE FEE + PENALTY AMOUNT PAID ---------------->'

test={
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

class OwnerBreakdown(object):
    json = {}

    def __init__(self, in_json):
        """json structure example for an owner

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
        self.json = munch.munchify(in_json)
        for k,v in self.json.iteritems():
            setattr(self, k, v)

        if not 'year' in self.json:
            self.json['year'] = utils.LAST_YEAR

    @property
    def pins(self):
        """return a list of all unique Parcel ID's"""
        return sorted(list(set([p.pin for p in iter(self)])))

    @property
    def cleanPINs(self):
        """returns a list of clean PINs (no special characters or spaces)"""
        return [utils.getPIN(p) for p in self.pins]

    def getCleanPINsInSection(self, section):
        """gets a list of PINs within a section

        Required:
            section -- section township range code
        """
        thePins = []
        for par in iter(self):
            if par[SECTION] == section:
                thePins.append(utils.getPIN(par['pin']))

        return sorted(list(set(thePins)))


    @property
    def parcelCount(self):
        """return count of parcels, differnt from number of assessments.  Will count
        number of unique parcels"""
        return len(self.pins)

    def sum(self, attr):
        """summarizes attributes from all assessments

        Required:
            attribute to summarize based on, must be one of these values:

        (ACRES|BENEFITS|DRAINAGE FEE AMOUNT)
        """
        valid = ['ACRES', 'BENEFITS', 'DRAINAGE FEE AMOUNT']
        if attr.upper() not in valid:
            return 0
        try:
            return sum(parcel.get(attr.upper(), 0) for parcel in iter(self))
        except KeyError:
            return 'N/A'

    def findSections(self):
        """return a unique value list of all sections where parcels are found"""
        return filter(lambda s: s != '99-99-99', sorted(list(set(parcel.get(SECTION, '99-99-99') for parcel in iter(self)))))

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

class Owners(object):
    """class to handle landowners for a county"""
    def __init__(self, owners={}):
        self.county = owners.items()[0][1].county
        self.owners = {k: OwnerBreakdown(v) for k,v in owners.iteritems()}
        self.count = len(self)
        self.codes = sorted(self.owners.keys())

    def find(self, code):
        """find owner by code"""
        return owners.get(code)

    def findByPID(self, pid):
        """find owner by parcel ID"""
        if pid:
            clean_pin = utils.getPIN(pid)
            for owner in iter(self):
                if clean_pin in owner.cleanPINs:
                    return owner

    def findByName(self, name):
        """find owner by name"""
        for owner in iter(self):
            if owner.name == name:
                return owner

    def __iter__(self):
        """generator for owners"""
        for code, owner in sorted(self.owners.iteritems()):
            yield owner

    def __getitem__(self, code):
        """get assessment by code"""
        return self.owners[code]

    def __len__(self):
        """count of owners in county"""
        return len(self.owners)

    def __nonzero__(self):
        """is not 0"""
        return bool(len(self))

    def __repr__(self):
        return '<Owners "{}">'.format(self.county)

def selectAndZoom(lyr, where, df, auto_refresh=False):
    """selects a layer and zooms to it"""
    arcpy.management.SelectLayerByAttribute(lyr, 'NEW_SELECTION', where)
    df.zoomToSelectedFeatures()
    arcpy.management.SelectLayerByAttribute(lyr, 'CLEAR_SELECTION')
    if auto_refresh:
        arcpy.RefreshActiveView()
    return

def getMXDPath():
    """finds the template mxd, unzips if necessary"""
    mapDoc = os.path.join(utils.DATA, 'Receipt', 'Receipt.mxd')
    if not os.path.exists(mapDoc):
        # unzip it from the bin folder
        z = mapDoc.replace('.mxd', '.zip')
        utils.unzip(z)

    return mapDoc

@utils.timeit
def generateOwnerReceiptsForCounty(out_folder, county, year=utils.LAST_YEAR, where_clause='', mail_to_name=DEFAULT_MAIL_NAME,
                                mail_to_addr=DEFAULT_MAIL_ADDR, mail_to_csz=DEFAULT_MAIL_CSZ, add_map_reports=False):
    """ Generates owner receipts for the entire county

    Required:


    Optional:

    """
    gdb = utils.Geodatabase()
    owners = Owners(gdb.getOwnerReceiptDict(county, year, where_clause))

    # mxd for reports
    mxd = None
    if add_map_reports in ('true', True):
        mapDoc = getMXDPath()

        # reference mxd
        mxd = arcpy.mapping.MapDocument(mapDoc)

        utils.Message('Generating Receipts with maps for {} land owners, this could take a while...'.format(len(owners)))

    else:
        utils.Message('Generating Receipts for {} land owners...'.format(len(owners)))

    # generate reports
    addresses = []
    for i, owner in enumerate(owners):
        generateOwnerReceipt(out_folder, owner, mail_to_name, mail_to_addr, mail_to_csz, add_map_reports, mxd)
        addresses.append([owner.name, owner.address, owner.csz])

        if not i % 100 and i > 1:
            utils.Message('Created reports {}-{} of {}...'.format(i - 99, i, len(owners)))

    utils.Message('Created reports {}-{}'.format((int(i/100) * 100) + 1, len(owners)))

    # generate mailing labels
    outPDF = os.path.join(out_folder, '{}_mailing.pdf'.format(county.replace(' ','_')))
    avery5160(outPDF, addresses)

    del mxd
    return

@utils.timeit
def generateOwnerReceiptByCode(out_folder, code, year=utils.LAST_YEAR, where_clause='', mail_to_name=DEFAULT_MAIL_NAME,
                                mail_to_addr=DEFAULT_MAIL_ADDR, mail_to_csz=DEFAULT_MAIL_CSZ, add_map_reports=False):
    """

    """
    gdb = utils.Geodatabase()
    owner_where = "CODE = '{}'".format(code)
    owners = Owners(gdb.getOwnerReceiptDict(year=year, where_clause=owner_where))

    # check for map reports
    mxd = None
    if add_map_reports in ('true', True):
        mapDoc = getMXDPath()

        # reference mxd
        mxd = arcpy.mapping.MapDocument(mapDoc)

    for owner in owners:

        # should just be one...
        generateOwnerReceipt(out_folder, owner, mail_to_name, mail_to_addr, mail_to_csz, add_map_reports, mxd)

    utils.Message('Generated owner receipt for landowner: "{}"'.format(code))
    #mxd.saveACopy(mxd.filePath.split('.' )[0] + '__2.mxd') # testing only....
    del mxd
    return

def generateOwnerReceipt(out_folder, owner_json, mail_to_name=DEFAULT_MAIL_NAME, mail_to_addr=DEFAULT_MAIL_ADDR,
                         mail_to_csz=DEFAULT_MAIL_CSZ, add_map_reports=False, mxd=None ):
    """ Generates receipt for a single owner with option to add map to report.

    ***Adding maps to the report signifcantly slows down the process***

    Required:

    Optional:

    """

    # **************************************************************************************
    # styles
    #
    # set up style dict
    styleDict = {ACRES: styleCurrency,
                 BENEFITS: styleCurrency,
                 DRAINAGE_FEE: styleCurrency,
                 DEFAULT_STYLE: defaultStyle
        }

    # Get column widths
    headers = [YEAR, SECTION, SEQUENCE, DESCRIPTION, ACRES, BENEFITS, DRAINAGE_FEE, BLANK]
    widths = (8, 8, 6, 30, 6, 8, 17, 15)

    col_widths = dict(zip(range(len(headers)), widths))


    # override styleHeadersWithBorder
    styleHeadersWithBorder.alignment = leftAlign

    # empty row with dashed underline
    emptyRowStyleDict = {DRAINAGE_FEE: yearBreak}


    # **************************************************************************************
    # header indices
    acre_ind = headers.index(ACRES)
    ben_ind = headers.index(BENEFITS)
    drainage_ind = headers.index(DRAINAGE_FEE)
    blank_ind = 7

    # data prep
    if not isinstance(owner_json, OwnerBreakdown) and isinstance(owner_json, dict):
        owner_json = OwnerBreakdown(owner_json)

    out_excel = os.path.join(out_folder, owner_json.code + '.xls')

    # map validation
    if add_map_reports in ('true', True):
        add_map_reports = True
        if not isinstance(mxd, arcpy.mapping.MapDocument):
            add_map_reports = False

    # new workbook
    wb = ExcelWorkbook()
    ws = wb.add_sheet('Receipt', headers, header_line_no=8, use_borders=False, styleHeaders=styleHeadersWithBorder,
                      styleDict=styleDict, widths=col_widths)

    # write merged and special header cells
    # top left portion
    ws.ws.write_merge(0, 0, 0, 3, '*** CURRENT DRAINAGE FEE {} ***'.format(owner_json.year), style=styleHeaders)
    ws.ws.write_merge(1, 1, 0, 3, 'COUNTY OF {}'.format(' '.join(owner_json.county.split()[:-1])), style=styleHeaders)
    ws.ws.write_merge(2, 2, 0, 3, 'LANDOWNER:    {}'.format(owner_json.code), style=styleHeaders)
    ws.ws.write_merge(4, 4, 0, 3, owner_json.name, style=styleHeaders)
    ws.ws.write_merge(5, 5, 0, 3, owner_json.address, style=styleHeaders)
    ws.ws.write_merge(6, 6, 0, 3, owner_json.csz, style=styleHeaders)

    # top center portion
    ws.ws.write_merge(0, 0, 4, 6, 'THE LITTLE RIVER DISTRICT', style=styleHeaders)
    ws.ws.write_merge(0, 0, 4, 6, 'THE LITTLE RIVER DISTRICT', style=styleHeaders)
    ws.ws.write_merge(2, 2, 4, 6, 'MAIL PAYMENT TO:', style=styleHeaders)
    ws.ws.write_merge(4, 4, 4, 6, mail_to_name, style=styleHeaders)
    ws.ws.write_merge(5, 5, 4, 6, mail_to_addr, style=styleHeaders)
    ws.ws.write_merge(6, 6, 4, 6, mail_to_csz, style=styleHeaders)

    # top right portion
    ws.ws.write(0, blank_ind, 'receipt    {}'.format(owner_json.code), style=styleHeadersRight)

    # override headers for numbers to use right alignment
    ws.ws.write(ws.header_line_no, acre_ind, ACRES, style=styleHeadersRight2)
    ws.ws.write(ws.header_line_no, ben_ind, BENEFITS, style=styleHeadersRight2)
    ws.ws.write(ws.header_line_no, drainage_ind, DRAINAGE_FEE, style=styleHeadersRight2)

    # add rows
    for assessment in owner_json.assessments:
        assessment[YEAR] = owner_json.year

        ws.addRow(**assessment)


    # add empty row and total row
    ws.addRow(styleDict=emptyRowStyleDict)
    ws._currentRowIndex += 1

    # create formula
    ri = ws._currentRowIndex
    col = ascii_uppercase[drainage_ind]
    form = '&TEXT(SUM({col}{st}:{col}{end}), "#,##0.00")'.format(col=col, st=ws.header_line_no+2, end=ri)
    totFormula = Formula('"TOTAL DRAINAGE FEE AMOUNT      "{}'.format(form))
    ws.ws.write_merge(ri, ri, 4, 6, totFormula, style=styleHeadersRight)

    # other merged cells
    ri += 1
    ws.ws.write_merge(ri, ri, 1, 6, PENALTY, style=styleHeadersRight)
    ws.ws.write(ri,7, ' ', style=yearBreak)
    ri += 1
    ws.ws.write_merge(ri, ri, 3, 6, TOT_PEN, style=styleHeadersRight)
    ws.ws.write(ri,7, ' ', style=yearBreak)
    ws._currentRowIndex = ri # just because it's the right thing to do...

    # set print properties
    ws.ws.set_fit_width_to_pages(1)
    ws.ws.set_fit_height_to_pages(0)
    ws.ws.set_portrait(0)
    ws.ws.set_fit_num_pages(1)

    # set page headers
    ws.ws.set_header_str('&R Page &P of &N')
    footer = unicode('Receipt {} for Landowner {}'.format(owner_json.code, owner_json.name))
    ws.ws.set_footer_str(footer)

    # save it
    wb.save(out_excel)
    del wb

    # **************************************************************************************
    #
    # do map report
    pdfDoc = None
    if add_map_reports and isinstance(mxd, basestring) and os.path.exists(mxd):
        mxd = arcpy.mapping.MapDocument(mxd)

    if add_map_reports and isinstance(mxd, arcpy.mapping.MapDocument):
        gdb = utils.Geodatabase()
        symb_lyr = os.path.join(utils.DATA, 'Selected Parcels.lyr')
        out_pdf = os.path.join(out_folder, owner_json.code + '.pdf')
        pdfDoc = arcpy.mapping.PDFDocumentCreate(out_pdf)

        # get layer list
        df_main = arcpy.mapping.ListDataFrames(mxd, 'Layers')[0]
        df_ov = arcpy.mapping.ListDataFrames(mxd, 'District Overview')[0]
        df_sel = arcpy.mapping.ListDataFrames(mxd, 'Selected County')[0]

        layers_main = arcpy.mapping.ListLayers(mxd, '*', data_frame=df_main)
        layers_ov = arcpy.mapping.ListLayers(mxd, '*', data_frame=df_ov)
        layers_sel = arcpy.mapping.ListLayers(mxd, '*', data_frame=df_sel)

        # find layers
        parcels_fc = gdb.getParcelPath(owner_json.county)
        parcels_lyr = [l for l in layers_main if l.name.title() == owner_json.county.title() + ' Parcels'][0]
        selected_pars = [l for l in layers_main if l.name.title() == owner_json.county.title() + ' Selection'][0]
        county_dis = [l for l in layers_ov if l.name == 'Selected County District'][0]
        county_inset = [l for l in layers_sel if l.name == 'Selected County Inset'][0]

        # reference text elements
        elms = arcpy.mapping.ListLayoutElements(mxd, 'TEXT_ELEMENT')
        owner_code_elm = [e for e in elms if e.name == 'OWNER_CODE'][0]
        sec_elm = [e for e in elms if e.name == 'SECTION_LABEL'][0]
        owner_elm = [e for e in elms if e.name == 'OWNER_INFO_LABEL'][0]
        district_elm = [e for e in elms if e.name == 'DISTRICT_LABEL'][0]
        county_elm = [e for e in elms if e.name == 'COUNTY_INSET_LABEL'][0]

        # set up some initial text elements
        owner_code_elm.text = 'Owner Code: {}'.format(owner_json.code)
        owner_elm.text = '\r\n'.join([owner_json.name, owner_json.address, owner_json.csz])
        tot_drain = 'TOTAL DRAINAGE FEE:  {:.2f}'.format(owner_json.sum(DRAINAGE_FEE))
        tot_acre = 'TOTAL ACRES:  {:.2f}'.format(owner_json.sum(ACRES))
        district_elm.text = '\r\n'.join([owner_json.county, tot_drain, tot_acre])
        county_elm.text = owner_json.county.title()

        # iterate though sections to select parcels
        own_where = "{} = '{}'".format(utils.OWNER_CODE, owner_json.code)

        hasPages = False
        for sec in owner_json.findSections():

            # add pin filter
            pin_tuple = tuple(str(utils.getPIN(p)) for p in owner_json.getCleanPINsInSection(sec))
            if len(pin_tuple) > 0:
                if len(pin_tuple) == 1:
                    pin_tuple = "('{}')".format(pin_tuple[0])
                pin_where = " OR {} IN {}".format(utils.PIN, pin_tuple)
            else:
                pin_where = ''

            # final wehre
            sec_where = "{} = '{}'".format(SEC_TWN_RNG_GIS, sec)
            where = ' AND '.join([own_where, sec_where]) + pin_where
            print where

            # make a feature layer
            selected_pars.definitionQuery = where
            selected_pars.visible = True
            selectionCount = int(arcpy.management.GetCount(selected_pars).getOutput(0))
            if selectionCount >= 1:
                hasPages = True

                # zoom to selected parcels
                selectAndZoom(selected_pars, 'OBJECTID IS NOT NULL', df_main)
                if selectionCount == 1:
                    df_main.scale *= 1.25

                # zoom to county in county inset map
                sec_elm.text = sec
                county_query = "NAME = '{}'".format(owner_json.county)
                county_dis.definitionQuery = county_query
                county_inset.definitionQuery = county_query
                selectAndZoom(county_inset, county_query, df_sel)

                # export to PDF
                arcpy.RefreshActiveView()
                tmpPDF = os.path.join(out_folder, 'tmp.pdf')
                arcpy.mapping.ExportToPDF(mxd, tmpPDF, resolution=125)

                # add to master pdf and clean up
                pdfDoc.appendPages(tmpPDF)
                os.remove(tmpPDF)

        # return outputs
        if pdfDoc and hasPages:
            pdfDoc.saveAndClose()
            del pdfDoc

    return
