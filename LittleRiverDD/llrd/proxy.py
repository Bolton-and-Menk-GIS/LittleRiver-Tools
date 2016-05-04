#-------------------------------------------------------------------------------
# Name:        Proxy
# Purpose:
#
# Author:      Caleb Mackey
#
# Created:     03/03/2016
# Copyright:   (c) Bolton & Menk, Inc. 2016
#-------------------------------------------------------------------------------
from . import utils
from .proxy_strings import *
import datetime
import time
import os
import arcpy
import shutil
import tempfile
import calendar
from .mailing import avery5160

# env
arcpy.env.overwriteOutput = True

# defaults
DEFAULT_DATE = datetime.datetime(int(time.strftime('%Y')) - 1, 12, 15)
DEFAULT_CITY = 'Wardell'
DEFAULT_COUNTY = 'Pemiscot County'

def getProxyMXD():
    """gets the proxy mxd"""
    tmp = tempfile.mkdtemp()
    mxd_zip = os.path.join(utils.DATA, 'Proxy.zip')
    mxd_copy = os.path.join(tmp, 'Proxy.mxd')
    utils.unzip(mxd_zip, tmp)
    return arcpy.mapping.MapDocument(mxd_copy)

@utils.timeit
def generateProxyBallots(out_folder, county, meeting_city=DEFAULT_CITY, meeting_county=DEFAULT_COUNTY, meeting_date=DEFAULT_DATE):
    """generate proxy reports for each owner

    Required:
        out_folder -- output folder location for all proxy ballots
        county -- name of county to generate proxy for

    Optional:
        meeting_city -- name of city where meeting will occur
        meeting_county -- name of county where meeting will occur
        meeting_date -- date of meeting as datetime.datetime() object
    """
    # get date
    day = meeting_date.day
    month = meeting_date.month
    year = meeting_date.year

    # get Landowners object
    gdb = utils.Geodatabase()
    landowners = gdb.getOwners(county)

    # get proxy template
    mxd = getProxyMXD()
    textElms = {e.name: e for e in arcpy.mapping.ListLayoutElements(mxd, 'TEXT_ELEMENT') if e.name}
    dateElm = textElms['dateElm']
    ownerAcres = textElms['ownerAcres']
    ownerMailing = textElms['ownerMailing']
    textBox = textElms['textBox']

    # mailing labels
    addresses = []

    # create master PDF file
    finalPDF = arcpy.mapping.PDFDocumentCreate(os.path.join(out_folder, '{}_Proxy.pdf'.format(county.replace(' ','_'))))

    # iterate through landowners and generate proxy for each one
    for i,owner in enumerate(landowners[:75]):
        out_pdf = os.path.join(out_folder, owner.code + '_proxy.pdf')

        # set text elms
        dateElm.text = DATE_ELM.format(MONTH=calendar.month_name[month], YEAR=year)
        textBox.text = TEXTBOX_ELM.format(COUNTY=meeting_county.title(), CITY=meeting_city.title(),
                                          DAY=day, MONTH=calendar.month_name[month], YEAR=year)
        multi_line_owner = '\r\n'.join(filter(None, [owner.name, owner.name2]))
        ownerMailing.text = OWNER_ELM.format(OWNER=multi_line_owner, ADDRESS=owner.address,
                                             CITY_ST_ZIP=owner.address_suffix if owner.address_suffix != None else ' ')
        ownerAcres.text = ACRES_ELM.format(OWNER_CODE=owner.code, ACRES=round(owner.sum('assessed_acres'), 1))

        # export to PDF
        arcpy.mapping.ExportToPDF(mxd, out_pdf, resolution=125)

        # add mailing label
        addresses.append([multi_line_owner, owner.address, owner.address_suffix])

        # add to final PDF
        finalPDF.appendPages(out_pdf)
        try:
            os.remove(out_pdf)
        except:
            pass

        pdfCount = i + 1
        if pdfCount %100 == 0:
            utils.Message('Generated Proxy Ballots {}-{} of {}'.format(pdfCount-99, pdfCount, landowners.count))

##    if pdfCount != landowners.count:
##        utils.Message('Generated Proxy Ballots {}-{}'.format(pdfCount+1, landowners.count))


    # clean up
    finalPDF.saveAndClose()
    mxd_path = mxd.filePath
    directory = os.path.dirname(mxd_path)
    del mxd
    del finalPDF

    # generate mailing labels
    out_labels = os.path.join(out_folder, '{}_MailingLabelsProxy.pdf'.format(county.replace(' ','_')))
    avery5160(out_labels, addresses)

    # delete temp files
    arcpy.management.Delete(mxd_path)
    shutil.rmtree(directory, True)
    return landowners