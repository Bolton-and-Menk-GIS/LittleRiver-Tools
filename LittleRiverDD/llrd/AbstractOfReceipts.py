#-------------------------------------------------------------------------------
# Name:        Abstract of Receipts
# Purpose:
#
# Author:      Caleb Mackey
#
# Created:     02/29/2016
# Copyright:   (c) Bolton & Menk, Inc. 2016
#-------------------------------------------------------------------------------
from . import excel
import xlwt
reload(excel)
from excel import *
from excel_styles import *
from . import utils
import os
import arcpy
arcpy.env.overwriteOutput = True
from string import ascii_uppercase

DATE_PAID = 'DATE PAID'
LANDOWNER = 'LANDOWNER NAME'
CODE = 'CODE'
SECTION = 'SC'
TOWNSHIP = 'TN'
RANGE = 'RG'
SEQUENCE = 'SEQ'
YEAR = 'YEAR'
TAX_PAID = 'TAX PAID'
PENALTY = 'PENALTY'
EXCESS = 'EXCESS'
TOTAL_COLLECTION = 'TOTAL COLLECTION'

# fields from Geodatabase.summary_table
CODE_FC = utils.OWNER_CODE
AMOUNT_PAID_FC = 'AMOUNT_PAID'
PENALTY_FC = 'PENALTY'
EXCESS_FC = 'EXCESS'
YEAR_FC = 'YEAR'
DATE_PAID_FC = 'DATE_PAID'
OWNER_FC = 'OWNER'
SECTION_FC = 'SECTION'
TOWNSHIP_FC = 'TOWNSHIP'
RANGE_FC = 'RANGE'
SEQUENCE_FC = 'SEQUENCE'
COUNTY_FC = 'COUNTY'


##@utils.timeit
def generateAOR(out_excel, county, where_clause=None, sort_by=utils.OWNER_CODE):
    """generate Abstract of Receipts report in excel format

    Required:
        out_excel -- output excel workbook with .xls file extension
        county -- name of county

    Optional:
        where_clause -- optional where clause to pull out only specific records
        sorty_by -- attributes to sort by
    """
    if os.path.exists(out_excel):
        os.remove(out_excel)

    # **************************************************************************************
    # styles
    #
    # set up style dict
    styleDict = {DATE_PAID: styleDate,
                 LANDOWNER: styleHeadersLeft,
                 CODE: defaultStyle,
                 SECTION: zfillStyle,
                 TOWNSHIP: zfillStyle,
                 RANGE: zfillStyle,
                 SEQUENCE: defaultStyle,
                 YEAR: defaultStyle,
                 TAX_PAID: styleCurrency,
                 PENALTY: styleCurrency,
                 EXCESS: styleCurrency,
                 TOTAL_COLLECTION: styleCurrency
        }

    # style dict for breaking out of years
    yearBreakDict = {TAX_PAID: yearBreak,
                      PENALTY: yearBreak,
                      EXCESS: yearBreak,
                      TOTAL_COLLECTION: yearBreak
        }


    # column widths
    widths = (12, 8, 35, 4, 4, 4, 7, 9, 9, 7, 7, 10)

    # **************************************************************************************

    # validate table name and set up workbook and sheets
    if not os.path.splitext(out_excel)[-1] == '.xls':
        out_excel = os.path.splitext(out_excel)[0] + '.xls'

    headers = [DATE_PAID,CODE, LANDOWNER, SECTION, TOWNSHIP, RANGE, SEQUENCE,
                YEAR, TAX_PAID, PENALTY, EXCESS, TOTAL_COLLECTION]

    col_widths = dict(zip(range(len(headers)), widths))

    # new workbook
    wb = ExcelWorkbook()
    ws = wb.add_sheet('Receipts', headers, header_line_no=4, use_borders=False, styleHeaders=styleHeadersWithBorder, styleDict=styleDict, widths=col_widths)

    # add date formula for first cell
    ws.ws.write(0, 0, Formula('TODAY()'), styleDate)

    # merge and center lines
    ws.ws.write_merge(0, 0, 1, 11, 'THE LITTLE RIVER DRAINAGE DISTRICT', style=styleHeaders) #was merged between 3 & 7
    ws.ws.write_merge(1, 1, 1, 11, 'ABSTRACT OF RECEIPTS', style=styleHeaders)
    ws.ws.write_merge(2, 2, 0, 2, 'COUNTY OF {}'.format(' '.join(county.upper().split()[:-1])), style=styleHeadersLeft)
    ws.ws.write_merge(2, 2, 10, 11, None, style=underline)
    ws.ws.write_merge(2, 2, 8, 9, 'ABSTRACT NO.', style=styleHeadersRight)

    # form sql clause, make sure it is sorted by year at minimum
    sql = (None, None)
    if sort_by in(None, '', '#'):
        sort_by = utils.OWNER_CODE
    if sort_by:
        sql = (None, 'ORDER BY {}'.format(', '.join(sort_by.split(';'))))

    # fields from Geodatabase.summary_table
    fields = [DATE_PAID_FC, utils.OWNER_CODE, OWNER_FC, SECTION_FC, TOWNSHIP_FC, RANGE_FC,
              SEQUENCE_FC, YEAR_FC, AMOUNT_PAID_FC, PENALTY_FC, EXCESS_FC]

    # indices, use these in case field order changes
    assessment_ind = len(fields) - 1
    year_ind = fields.index(YEAR_FC)
    amount_ind = fields.index(AMOUNT_PAID_FC)
    penalty_ind = fields.index(PENALTY_FC)
    excess_ind = fields.index(EXCESS_FC)

    # indices for spreadsheet fields
    sci, tni, rgi = (headers.index(SECTION), headers.index(TOWNSHIP), headers.index(RANGE))

    # get last year
    nye_prior_year = datetime.datetime(datetime.datetime.now().year -1, 12, 31)
    year = nye_prior_year.year

    # alter initial where clause to include county
    where_clause = ' AND '.join(filter(None, ["{} = '{}'".format(COUNTY_FC, county.upper()), where_clause]))

    # iterate through summary table and make sure all years have been populated
    gdb = utils.Geodatabase()
    with arcpy.da.SearchCursor(gdb.summary_table, [YEAR_FC], where_clause) as rows:
        all_years = list(set(r[0] for r in rows))

##    all_years = []
##    with utils.UpdateCursor(gdb.summary_table, [YEAR_FC, DATE_PAID_FC], where_clause) as rows:
##        for r in rows:
##            if not r[0]:
##                r[0] = year
##
##            if not isinstance(r[1], datetime.datetime):
##                r[1] = nye_prior_year
##
##            rows.updateRow(r)
##
##            if r[0] not in all_years:
##                all_years.append(r[0])

    # set up where clause
    for yr in sorted(all_years):
        where = ' AND '.join(filter(None, [where_clause, "{} = {}".format(YEAR_FC, yr)]))
        cur_year_start = ws._currentRowIndex + 1

        # populate rows
        with arcpy.da.SearchCursor(gdb.summary_table, fields, where, sql_clause=sql) as rows:
            for r in rows:

                v = list(r)

                for i, val in enumerate(v):

                    # cast to int to apply number formatting
                    if i in (sci, tni, rgi):
                        if val is not None:
                            try:
                                val = int(val)
                                if val == 0:
                                    val = 99

                                v[i] = val
                            except ValueError:
                                v[i] = 99
                        else:
                            # default for null
                            v[i] = 99

                    elif i == 0 and val in (None, ''):
                        v[i] = nye_prior_year

                    if i == year_ind and not val:
                        v[i] = year

                # make a formula for total collection
                tot = Formula('({ac}{ri} + {pc}{ri}) - {ec}{ri}'.format(ri=ws._currentRowIndex+1,
                                                                        ac=ascii_uppercase[amount_ind],
                                                                        pc=ascii_uppercase[penalty_ind],
                                                                        ec=ascii_uppercase[excess_ind]))

                v.append(tot)

                # add row
                ws.addRow(*v)

        # add blank row with dashed style
        ws.addRow(styleDict=yearBreakDict)

        # now add totals
        totals = {h:Formula('SUM({col}{st}:{col}{en})'.format(col=ascii_uppercase[i],
                st=cur_year_start, en=ws._currentRowIndex-1))
                for i,h in enumerate(headers) if i >= amount_ind}

        totals[YEAR] = '{} TOTAL'.format(yr)
        ws.addRow(**totals)

        # add another blank row
        ws._currentRowIndex += 1

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
    os.startfile(out_excel)
    del wb
    return out_excel