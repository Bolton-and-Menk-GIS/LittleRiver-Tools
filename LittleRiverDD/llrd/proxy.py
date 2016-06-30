import datetime
import time
import math
import os
import calendar
from .mailing import avery5160
import sys
import textwrap
from . import utils
sys.path.append(utils.THIRD_PARTY)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Courier New', 'cour.ttf'))


BODY_ELM = 'I, {SHORT_LINE}, hearby appoint {SHORT_LINE} as my attorney to represent me ' + \
            'at the annual meeting of the landowners of the Little River Drainage District ' + \
            'to be held in the city of {CITY}, {COUNTY}, MO, on the {DAY} of {MONTH}, {YEAR}.  ' + \
            'I hereby authorize my proxy to cast my votes at said meeting or election to which ' + \
            'I am entitled under the law to vote for'

BODY_ELM2 = 'as Supervisor of said District for an expired five (5) year term.'

DATE_ELM = u'PROXY for the LITTLE RIVER DRAINAGE DISTRICT           _____________ day of {MONTH}, {YEAR}'
ACRES_ELM = u'{OWNER_CODE} Total ACRES owned in the District =  {ACRES}'
OWNER_ELM = u'{OWNER}\r\n{ADDRESS}\r\n{CITY_ST_ZIP}'
SHORT = '_' * 27
LONG = '_' * 48
SIG_LINE = '_' * 30

# defaults
DEFAULT_DATE = datetime.datetime(int(time.strftime('%Y')) - 1, 12, 15)
DEFAULT_CITY = 'Wardell'
DEFAULT_COUNTY = 'Pemiscot County'

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
    calander_month = calendar.month_name[month]
    date_string = '     _____________ day of {MONTH}, {YEAR}'.format(MONTH=calander_month, YEAR=year)

    # get Landowners object
    gdb = utils.Geodatabase()
    landowners = gdb.getOwners(county)

    out_pdf_path = os.path.join(out_folder, '{}_Proxy.pdf'.format(county.replace(' ','_')))
    if os.path.exists(out_pdf_path):
        try:
            os.remove(out_pdf_path)
        except:
            pass

    # having issues deleting sometimes, make sure we have a unique file name...
    out_pdf_path = utils.assignUniqueName(out_pdf_path)

    c = canvas.Canvas(out_pdf_path, pagesize=letter)

    # set up canvas
    title_hz = 2.0 * inch
    title_vt = 10.7 * inch
    body_hz = 0.4 * inch
    body_vt = 9.9 * inch
    owner_hz = 1.0 * inch
    owner_vt = 8.25 * inch
    acre_hz = 5.2 * inch
    acre_vt = 8.25 * inch
    sig_hz = 4.5 * inch
    sig_vt = 7.3 * inch

    # iterate through landowners and generate proxy for each one
    addresses = []
    for owner in landowners:

        c.setFont('Courier New', 11)

        # set to initial position for title
        label = c.beginText()
        label.setTextOrigin(title_hz, title_vt)
        title_lines = ['PROXY for the LITTLE RIVER DRAINAGE DISTRICT', ' ', date_string]
        label.textLines(title_lines, 0)
        c.drawText(label)

        # move to position for body
        body = c.beginText()
        body.setTextOrigin(body_hz, body_vt)
        body_text = BODY_ELM.format(COUNTY=meeting_county.title(), CITY=meeting_city.title(), DAY=day,
                                     MONTH=calendar.month_name[month], YEAR=year, SHORT_LINE=SHORT)
        first_part = textwrap.wrap(body_text, 75)
        body.textLines(first_part + [' ' * (len(first_part[-1]) + 1) + LONG, BODY_ELM2])
        c.drawText(body)

        # move to position for owner info
        owner_label = c.beginText()
        owner_label.setTextOrigin(owner_hz, owner_vt)
        multi_line_owner = '\r\n'.join(filter(None, [owner.name, owner.name2]))
        owner_lines = filter(None, [owner.name, owner.name2, owner.address,
                            owner.address_suffix if owner.address_suffix != None else ' '])
        owner_label.textLines(owner_lines)
        c.drawText(owner_label)

        # move to position for acre info
        acre_label = c.beginText()
        acre_label.setTextOrigin(acre_hz, acre_vt)
        acre_lines = [owner.code, 'Total ACRES owned', 'in the District ={:6}'.format(int(math.floor(owner.sum('assessed_acres'))))]
        acre_label.textLines(acre_lines)
        c.drawText(acre_label)

        # move to position for signature
        sig_label = c.beginText()
        sig_label.setTextOrigin(sig_hz, sig_vt)
        sig_label.textLines([SIG_LINE, 'SIGNATURE OF LANDOWNER'])
        c.drawText(sig_label)

        # page break
        c.showPage()

        # add to addresses
        addresses.append([multi_line_owner, owner.address, owner.address_suffix])

    c.save()
    del c

    # generate mailing labels
    out_labels = os.path.join(out_folder, '{}_MailingLabelsProxy.pdf'.format(county.replace(' ','_')))
    avery5160(out_labels, addresses)
    return out_pdf_path

