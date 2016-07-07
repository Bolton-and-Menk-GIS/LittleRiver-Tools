#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     15/04/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from . import excel
import xlwt
reload(excel)
from excel import *
from excel_styles import *
from . import utils
from ._defaults import *
import os
import arcpy
arcpy.env.overwriteOutput = True
from string import ascii_uppercase
import sys
sys.path.append(utils.THIRD_PARTY)
from comtypes.client import CreateObject

# spreadsheet headers
CODE = 'CODE'
LANDOWNER = 'LANDOWNER NAME'
SECTION = 'SECTION'
SEQUENCE = 'SEQUENCE'
DESCRIPTION = 'DESCRIPTION'
PID = 'COUNTY MAP NUMBER'
ACRES = 'ACRES'
BENEFIT = 'BENEFIT'
ASSESSMENT = 'ASSESSMENT'
ADMIN_FEE = 'ADMIN FEE'
EXEMPT = 'E'
DATE_PAID = 'DATE PAID'

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
PIN = 'PIN'

# defaults and constants
DEFAULT_SORT = ';'.join([PID_GIS, CODE_GIS])
ADMINISTRATIVE_FEE = 'ADMINISTRATIVE FEE'
no_flag = "FLAG = 'N'"

# admin fee formula for spreadsheets
# use .format(b='C19', r=10) # where b is benefit and r is rate
ADMIN_FEE_FORMULA = 'IF(27.5-({b}*{r}) > 0, 27.5-({b}*{r}), 0)'
ADMIN_FEE_FORMULA = 'IF(27.5 - {a} > 0, 27.5 - {a}, 0)'
ASSESSMENT_FORMULA = '({b}*{r})'


def generateMAL_cs(out_excel, county, rate=10.0, year=2015, where_clause='', sort_by=DEFAULT_SORT):
    """wrapper function to do correct MAL report based on county"""
    if county.upper() in ALL_OR_NOTHING_COUNTIES:
        return generateMAL_AON_cs(out_excel, county, rate, year, where_clause, sort_by)
    else:
        return generateMAL_TOP_cs(out_excel, county, rate, year, where_clause, sort_by)

def generateMAL_AON_cs(out_excel, county, rate=10.0, year=2015, where_clause='', sort_by=DEFAULT_SORT):
    """Generates the Maintenance Assessment List for a county as an excel file using ALL_OR_NOTHING
    style of admin fees.

    Required:
        out_excel -- output .xls file
        county -- name of county
        rate -- tax rate for county as a float
        year -- year for assessment

    Optional:
        where_clause -- optional where clause to filter records
        sort_by -- optional fields to sort by, if none specified will sort by
            owner code and legal description (records are already sorted by
            section-township-range)
    """
    rate = float(rate)
    if os.path.exists(out_excel):
        os.remove(out_excel)

    # **************************************************************************************
    # styles
    #
    # set up style dict
    styleDict = {DATE_PAID: styleDate,
                 LANDOWNER: styleHeadersLeft,
                 ACRES: styleCurrency,
                 BENEFIT: styleCurrency,
                 ASSESSMENT: styleCurrency,
                 ADMIN_FEE: styleCurrency,
                 DEFAULT_STYLE: defaultStyle
        }

    # style dict for breaking out of years
    yearBreakDict = {ACRES: yearBreak,
                     BENEFIT: yearBreak,
                     ASSESSMENT: yearBreak,
                     ADMIN_FEE: yearBreak
        }

    # section overwrite style dict
    sectionBreakDict = {PID: styleHeadersRight}

    # column widths
    widths = (8, 35, 8, 9, 30, 20, 8, 8, 10, 10, 3, 8)

    # **************************************************************************************

    # validate table name and set up workbook and sheets
    if not os.path.splitext(out_excel)[-1] == '.xls':
        out_excel = os.path.splitext(out_excel)[0] + '.xls'

    headers = [CODE, LANDOWNER, SECTION, SEQUENCE, DESCRIPTION,
               PID, ACRES, BENEFIT, ASSESSMENT, ADMIN_FEE, EXEMPT, DATE_PAID]

    col_widths = dict(zip(range(len(headers)), widths))

    # new workbook
    wb = ExcelWorkbook()
    ws = wb.add_sheet('Assessments', headers, header_line_no=3, use_borders=False, styleHeaders=styleHeadersWithBorder,
                      styleDict=styleDict, widths=col_widths)

    # write merged and special header cells
    ws.ws.write(0, 0, Formula('TODAY()'), styleDate)
    ws.ws.write_merge(0, 0, 1, 7, 'THE LITTLE RIVER DRAINAGE DISTRICT', style=styleHeaders)
    ws.ws.write_merge(1, 1, 1, 7, 'MAINTENANCE ASSESSMENT LIST', style=styleHeaders)
    ws.ws.write_merge(0, 0, 9, 11, '{} {}'.format(year, ' '.join(county.upper().split()[:-1])), style=styleHeaders)
    ws.ws.write_merge(1, 1, 9, 11, 'RATE    %.1f' %float(rate) + '%', style=styleHeaders)

    # form sql clause, make sure it is sorted by year at minimum
    sql = (None, None)
    if sort_by in(None, '', '#'):
        sort_by = DEFAULT_SORT

    # make sure it is sorted by Section-Township-Range at minimum
    sql2 = (None, 'ORDER BY {}'.format(', '.join(sort_by.split(';') if isinstance(sort_by, basestring) else sort_by)))
    sort_fields = sort_by.split(';') if isinstance(sort_by, basestring) else sort_by
    if sort_by:
        sql = (None, 'ORDER BY {}'.format(', '.join(sort_fields)))
    print sql


    # default value for DATE PAID
    default_date_paid = datetime.datetime(int(year), 12, 31)

    # reference Geodatabase and fields
    county_where = "{} = '{}'".format(COUNTY_GIS, county.upper())
    gdb = utils.Geodatabase()
    fields = [CODE_GIS, LANDOWNER_GIS, SEC_TWN_RNG_GIS, SEQUENCE_GIS, DESCRIPTION_GIS,
             PID_GIS, ACRES_GIS, BENEFIT_GIS, ASSESSMENT_GIS, EXEMPT_GIS, DATE_PAID_GIS]

    # field indices
    sec_ind = fields.index(SEC_TWN_RNG_GIS)
    acre_ind = fields.index(ACRES_GIS)
    benefit_ind = fields.index(BENEFIT_GIS)
    assessment_ind = fields.index(ASSESSMENT_GIS)
    exempt_ind = fields.index(EXEMPT_GIS)
    date_ind = fields.index(DATE_PAID_GIS)
    desc_ind = fields.index(DESCRIPTION_GIS)
    seq_ind = fields.index(SEQUENCE_GIS)
    admin_ind = headers.index(ADMIN_FEE)
    ben_col = ascii_uppercase[headers.index(BENEFIT)]
    assess_col = ascii_uppercase[headers.index(ASSESSMENT)]

    # alter initial where clause to include county
    hide_admin = " AND {} <> '{}'".format(DESCRIPTION_GIS, ADMINISTRATIVE_FEE)
    null_secs = " AND {} NOT LIKE '%99%'".format(SEC_TWN_RNG_GIS)
    where_clause = ' AND '.join(filter(None, [county_where, where_clause, no_flag]))

    # admin fees
    #
    # recalculate admin fees if necessary
    #
    if float(rate) != float(utils.getRate()):
        gdb.calculate_admin_fee(rate)

    # now add rows to spreadsheet
    all_pins = {}
    grand_tots = {ACRES: [], BENEFIT: [], ASSESSMENT: [], ADMIN_FEE: []}

    start_index_row = ws._currentRowIndex + 1

    with arcpy.da.SearchCursor(gdb.breakdown_table, fields + [PIN], where_clause=where_clause, sql_clause=sql) as rows:
        cnt = 0
        for r in rows:

            vals = list(r)[:len(fields)]
            vals[headers.index(ASSESSMENT)] = Formula(ASSESSMENT_FORMULA.format(b='%s%s' %(ben_col, ws._currentRowIndex+1), r=(float(rate) * 0.01)))
            vals.insert(admin_ind, Formula(ADMIN_FEE_FORMULA.format(a='%s%s' %(assess_col, ws._currentRowIndex+1))))

            ws.addRow(*vals)
            all_pins[r[-1]] = vals
            cnt += 1

    # add blank row with dashed style
    ws.addRow(styleDict=yearBreakDict)

    # now add totals
    totals = {h:Formula('SUM({col}{st}:{col}{en})'.format(col=ascii_uppercase[i],
            st=start_index_row, en=ws._currentRowIndex-1))
            for i,h in enumerate(headers) if i in range(acre_ind, admin_ind+1)}

    totals[PID] = 'TOTAL'
    totals['styleDict'] = sectionBreakDict
    ws.addRow(**totals)
    for k in [ACRES, BENEFIT, ASSESSMENT, ADMIN_FEE]:
        grand_tots[k].append(totals[k])

    # add another blank row
    ws._currentRowIndex += 1

##    # now add grand totals
##    totals = {k: Formula(' + '.join([f.text() for f in v])) for k,v in grand_tots.iteritems()}
##
##    totals[PID] = 'GRAND TOTAL'
##    totals['styleDict'] = sectionBreakDict
##    ws.addRow(**totals)


    # set print properties
    ws.ws.set_fit_width_to_pages(1)
    ws.ws.set_fit_height_to_pages(0)
    ws.ws.set_portrait(0)
    ws.ws.set_fit_num_pages(1)

    # set page headers
    ws.ws.set_header_str('&R Page &P of &N')
    ws.ws.set_footer_str('')

    # save it
    wb.save(out_excel)
    del wb

    # add title rows
    xl = CreateObject('Excel.application')
    wb = xl.Workbooks.Open(out_excel)
    ws = wb.ActiveSheet
    ws.PageSetup.PrintTitleRows = '$1:$4'
    try:
        # silence compatibility message going from xls to xlsx
        wb.DoNotPromptForConvert = True
        wb.CheckCompatibility = False
        xl.DisplayAlerts = False
    except:
        pass
    wb.Save()
    wb.SaveAs(out_excel)
    wb.Close()
    xl.Application.Quit()
    del xl, wb

    os.startfile(out_excel)
    return out_excel

def generateMAL_TOP_cs(out_excel, county, rate=10.0, year=2015, where_clause='', sort_by=DEFAULT_SORT):
    """Generates the Maintenance Assessment List for a county as an excel file using TOTAL_OF_PARCELS
    style admin fees.

    Required:
        out_excel -- output .xls file
        county -- name of county
        rate -- tax rate for county as a float
        year -- year for assessment

    Optional:
        where_clause -- optional where clause to filter records
        sort_by -- optional fields to sort by, if none specified will sort by
            owner code and legal description (records are already sorted by
            section-township-range)
    """
    rate = float(rate)
    if os.path.exists(out_excel):
        os.remove(out_excel)

    # **************************************************************************************
    # styles
    #
    # set up style dict
    styleDict = {DATE_PAID: styleDate,
                 LANDOWNER: styleHeadersLeft,
                 ACRES: styleCurrency,
                 BENEFIT: styleCurrency,
                 ASSESSMENT: styleCurrency,
                 DEFAULT_STYLE: defaultStyle
        }

    # style dict for breaking out of years
    yearBreakDict = {ACRES: yearBreak,
                     BENEFIT: yearBreak,
                     ASSESSMENT: yearBreak,
        }

    # section overwrite style dict
    sectionBreakDict = {PID: styleHeadersRight}

    # column widths
    widths = (8, 35, 8, 9, 30, 20, 8, 8, 10, 3, 8)

    # **************************************************************************************

    # validate table name and set up workbook and sheets
    if not os.path.splitext(out_excel)[-1] == '.xls':
        out_excel = os.path.splitext(out_excel)[0] + '.xls'

    headers = [CODE, LANDOWNER, SECTION, SEQUENCE, DESCRIPTION,
               PID, ACRES, BENEFIT, ASSESSMENT, EXEMPT, DATE_PAID]

    col_widths = dict(zip(range(len(headers)), widths))

    # new workbook
    wb = ExcelWorkbook()
    ws = wb.add_sheet('Assessments', headers, header_line_no=3, use_borders=False, styleHeaders=styleHeadersWithBorder,
                      styleDict=styleDict, widths=col_widths)

    # write merged and special header cells
    ws.ws.write(0, 0, Formula('TODAY()'), styleDate)
    ws.ws.write_merge(0, 0, 1, 7, 'THE LITTLE RIVER DRAINAGE DISTRICT', style=styleHeaders)
    ws.ws.write_merge(1, 1, 1, 7, 'MAINTENANCE ASSESSMENT LIST', style=styleHeaders)
    ws.ws.write_merge(0, 0, 8, 10, '{} {}'.format(year, ' '.join(county.upper().split()[:-1])), style=styleHeaders)
    ws.ws.write_merge(1, 1, 8, 10, 'RATE    %.1f' %float(rate) + '%', style=styleHeaders)

    # form sql clause, make sure it is sorted by year at minimum
    sql = (None, None)
    if sort_by in(None, '', '#'):
        sort_by = DEFAULT_SORT

    # make sure it is sorted by Section-Township-Range at minimum
    sql2 = (None, 'ORDER BY {}'.format(', '.join(sort_by.split(';') if isinstance(sort_by, basestring) else sort_by)))
    sort_fields = sort_by.split(';') if isinstance(sort_by, basestring) else sort_by
    if sort_by:
        sql = (None, 'ORDER BY {}'.format(', '.join(sort_fields)))
    print sql

    # default value for DATE PAID
    default_date_paid = datetime.datetime(int(year), 12, 31)

    # reference Geodatabase and fields
    county_where = "{} = '{}'".format(COUNTY_GIS, county.upper())
    gdb = utils.Geodatabase()
    fields = [CODE_GIS, LANDOWNER_GIS, SEC_TWN_RNG_GIS, SEQUENCE_GIS, DESCRIPTION_GIS,
             PID_GIS, ACRES_GIS, BENEFIT_GIS, ASSESSMENT_GIS, EXEMPT_GIS, DATE_PAID_GIS]

    # field indices
    sec_ind = fields.index(SEC_TWN_RNG_GIS)
    acre_ind = fields.index(ACRES_GIS)
    benefit_ind = fields.index(BENEFIT_GIS)
    assessment_ind = fields.index(ASSESSMENT_GIS)
    exempt_ind = fields.index(EXEMPT_GIS)
    date_ind = fields.index(DATE_PAID_GIS)
    desc_ind = fields.index(DESCRIPTION_GIS)
    seq_ind = fields.index(SEQUENCE_GIS)
    ben_col = ascii_uppercase[headers.index(BENEFIT)]
    assess_col = ascii_uppercase[headers.index(ASSESSMENT)]

    # alter initial where clause to include county
    hide_admin = " AND {} <> '{}'".format(DESCRIPTION_GIS, ADMINISTRATIVE_FEE)
    null_secs = " AND {} NOT LIKE '%99%'".format(SEC_TWN_RNG_GIS)
    where_clause = ' AND '.join(filter(None, [county_where, where_clause, no_flag]))

    # now add rows to spreadsheet
    all_pins = {}
    grand_tots = {ACRES: [], BENEFIT: [], ASSESSMENT: []}

    start_index_row = ws._currentRowIndex + 1

    with arcpy.da.SearchCursor(gdb.breakdown_table, fields + [PIN], where_clause=where_clause, sql_clause=sql) as rows:
        for r in rows:

            vals = list(r)[:len(fields)]
            vals[headers.index(ASSESSMENT)] = Formula(ASSESSMENT_FORMULA.format(b='%s%s' %(ben_col, ws._currentRowIndex+1), r=(float(rate) * 0.01)))

            ws.addRow(*vals)
            all_pins[r[-1]] = vals

    # add blank row with dashed style
    ws.addRow(styleDict=yearBreakDict)

    # now add totals
    totals = {h:Formula('SUM({col}{st}:{col}{en})'.format(col=ascii_uppercase[i],
            st=start_index_row, en=ws._currentRowIndex-1))
            for i,h in enumerate(headers) if i in range(acre_ind, exempt_ind)}

    totals[PID] = 'TOTAL'
    totals['styleDict'] = sectionBreakDict
    ws.addRow(**totals)
    for k in [ACRES, BENEFIT, ASSESSMENT]:
        grand_tots[k].append(totals[k])

    # add another blank row
    ws._currentRowIndex += 1

    # now do admin fees
    #
    # recalculate admin fees if necessary
    #
    if float(rate) != float(utils.getRate()):
        gdb.calculate_admin_fee(rate)
        utils.Message('Adjusted Rate to: {}%'.format(rate))

    start_index_row = ws._currentRowIndex + 1

    # get owner summaries
    admin_fees = gdb.get_admin_fees(county_where)
    for code, atts in admin_fees.iteritems():
        if atts['total_admin_fee']:
            for assessment in atts['assessments']:
                vals = [None] * len(headers)
                vals[0] = atts['code']
                vals[1] = atts['name']
                vals[2] = '99-99-99'
                vals[seq_ind] = '9999'
                vals[desc_ind] = ADMINISTRATIVE_FEE
                vals[5] = assessment['pin']
                vals[6] = 0
                vals[7] = 0
                vals[8] = assessment['admin_fee']

                ws.addRow(*vals)

    # add blank row with dashed style
    ws.addRow(styleDict=yearBreakDict)

    # add another blank row
    ws._currentRowIndex += 1

    # now add grand totals
    totals = {h:Formula('SUM({col}{st}:{col}{en})'.format(col=ascii_uppercase[i],
            st=start_index_row, en=ws._currentRowIndex-1))
            for i,h in enumerate(headers) if i in range(acre_ind, exempt_ind)}

    totals[PID] = 'TOTAL for all Admin Fees'
    totals['styleDict'] = sectionBreakDict
    ws.addRow(**totals)
    for k in [ACRES, BENEFIT, ASSESSMENT]:
            grand_tots[k].append(totals[k])

    # add another blank row
    ws._currentRowIndex += 1

    # now add grand totals
    totals = {k: Formula(' + '.join([f.text() for f in v])) for k,v in grand_tots.iteritems()}

    totals[PID] = 'GRAND TOTAL'
    totals['styleDict'] = sectionBreakDict
    ws.addRow(**totals)


    # set print properties
    ws.ws.set_fit_width_to_pages(1)
    ws.ws.set_fit_height_to_pages(0)
    ws.ws.set_portrait(0)
    ws.ws.set_fit_num_pages(1)

    # set page headers
    ws.ws.set_header_str('&R Page &P of &N')
    ws.ws.set_footer_str('')

    # save it
    wb.save(out_excel)
    del wb

    # add title rows
    xl = CreateObject('Excel.application')
    wb = xl.Workbooks.Open(out_excel)
    ws = wb.ActiveSheet
    ws.PageSetup.PrintTitleRows = '$1:$4'
    try:
        # silence compatibility message saving as .xls
        wb.DoNotPromptForConvert = True
        wb.CheckCompatibility = False
    except:
        pass
    wb.Save()
    wb.Close()
    xl.Application.Quit()
    del xl, wb

    os.startfile(out_excel)
    return out_excel
