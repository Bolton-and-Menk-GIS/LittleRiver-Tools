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
import os
import arcpy
arcpy.env.overwriteOutput = True
from string import ascii_uppercase

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

# defaults and constants
DEFAULT_SORT = ';'.join([CODE_GIS, DESCRIPTION_GIS])
ADMINISTRATIVE_FEE = 'ADMINISTRATIVE FEE'

##@utils.timeit
def generateMAL(out_excel, county, rate=10.0, year=2015, where_clause='', sort_by=DEFAULT_SORT):
    """Generates the Maintenance Assessment List for a county as an excel file.

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
    sort_fields = [SEC_TWN_RNG_GIS] + sort_by.split(';') if isinstance(sort_by, basestring) else sort_by
    if sort_by:
        sql = (None, 'ORDER BY {}'.format(', '.join(sort_fields)))
    print sql


    # default value for DATE PAID
    default_date_paid = datetime.datetime(int(year), 12, 31)

    # reference Geodatabase and fields
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

    # alter initial where clause to include county
    hide_admin = " AND {} <> '{}'".format(DESCRIPTION_GIS, ADMINISTRATIVE_FEE)
    null_secs = " AND {} NOT LIKE '%99%'".format(SEC_TWN_RNG_GIS)
    where_clause = ' AND '.join(filter(None, ["{} = '{}'".format(COUNTY_GIS, county.upper()), where_clause]))

    # get sorted section-township-range
    utils.Message(fields)
    tv = arcpy.management.MakeTableView(gdb.breakdown_table, 'subset', where_clause + null_secs + hide_admin)
    with arcpy.da.SearchCursor(tv, fields, where_clause= where_clause + null_secs) as rows:
        sorted_plss = filter(None, sorted(list(set(r[sec_ind] for r in rows))))
    utils.Message('Cycling through {} Sections...'.format(len(sorted_plss)))

    # now add rows to spreadsheet
    for plss in sorted_plss:
        start_index_row = ws._currentRowIndex + 1

        # form where clause based on this section only
        where = ' AND '.join(filter(None, [where_clause, "{} = '{}'".format(SEC_TWN_RNG_GIS, plss)]))

        with arcpy.da.SearchCursor(gdb.breakdown_table, fields, where_clause=where, sql_clause=sql) as rows:
            for r in rows:

                # for some reason the cursor will not fetch records if this is added to
                #  the where clause...Bug???
                if r[desc_ind] != ADMINISTRATIVE_FEE:
                    # validate date paid
                    vals = list(r)

                    if not vals[date_ind]:
                        vals[date_ind] = default_date_paid
                    ws.addRow(*vals)


        # add blank row with dashed style
        ws.addRow(styleDict=yearBreakDict)

        # now add totals
        totals = {h:Formula('SUM({col}{st}:{col}{en})'.format(col=ascii_uppercase[i],
                st=start_index_row, en=ws._currentRowIndex-1))
                for i,h in enumerate(headers) if i in range(acre_ind, exempt_ind)}

        totals[PID] = 'TOTAL for Section {}'.format(plss)
        totals['styleDict'] = sectionBreakDict
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