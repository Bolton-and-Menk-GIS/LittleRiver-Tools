#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      calebma
#
# Created:     28/04/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from . import utils
import os
import arcpy
import sys
arcpy.env.overwriteOutput = True

FLAG_FIELDS = [('PIN', 'PIN', 'TEXT'),
               ('PIN_FLAG', 'PIN FLAG', 'TEXT'),
               ('CODE_FLAG', 'CODE FLAG', 'TEXT'),
               ('OWNER_FLAG', 'OWNER FLAG', 'TEXT'),
               ('ACRE_DIFFERENCE', 'ACRE DIFFERENCE', 'FLOAT'),
               ('ACRE_PER_DIFF', 'ACRE PERCENT DIFF', 'FLOAT'),
               ('BENEFIT_FLAG', 'BENEFIT FLAG', 'FLOAT'),
               ('ASSESSEMENT_FLAG', 'ASSESSMENT FLAG', 'FLOAT'),
               ('PLSS_FLAG', 'PLSS FLAG', 'TEXT'),
               ('COUNTY', 'COUNTY', 'TEXT'),
               ('COMMENTS', 'COMMENTS', 'TEXT')
            ]

##@utils.timeit
def getFlags(acre_threshold=10, min_acre_diff=40):
    """generates flags for *bad* records

    Optional:
        acre_threshold -- percentage between 1-100 to throw a flag if acre difference
            is off by >= this percentage.  Default is 10.
        min_acre_diff -- in addition to percent threshold, can also throw flags for
            acre differences >= this minimum acre difference.  Default is 40 acres.
    """
    acre_threshold = float(acre_threshold)
    min_acre_diff = float(min_acre_diff)
    if acre_threshold > 100 or acre_threshold == 0:
        raise ValueError('Acre threshold must be between 1-100!')

    if acre_threshold > 1:
        acre_threshold *= .01

    # run summary stats on breakdown table
    gdb = utils.Geodatabase()
    stats ='ACRES SUM;BENEFIT SUM;ASSESSMENT SUM;SEC_TWN_RNG FIRST'
    case_field='CODE;LANDOWNER_NAME;PIN;COUNTY'
    tmp_stats = r'in_memory\tmp_stats'
    #tmp_stats = os.path.join(gdb.path, 'tmp_stats') #testing only
    arcpy.analysis.Statistics(gdb.breakdown_table, tmp_stats, stats, case_field)

    # create new table
    if not arcpy.Exists(gdb.flag_table):
        flag_table_exists = False
        path, name = os.path.split(gdb.flag_table)
        arcpy.management.CreateTable(path, name)

        for fld, alias, ftype in FLAG_FIELDS:
            arcpy.management.AddField(gdb.flag_table, fld, ftype, field_alias=alias, field_length=255)

    else:
        # just clear out the rows
        flag_table_exists = True
        arcpy.management.DeleteRows(gdb.flag_table)

    # read summarized breakdown table
    sum_d = {}
    s_fields = ['PIN', 'CODE', 'LANDOWNER_NAME', 'SUM_ACRES', 'SUM_BENEFIT', 'SUM_ASSESSMENT', 'FIRST_SEC_TWN_RNG']
    with arcpy.da.SearchCursor(tmp_stats, s_fields) as rows:
        for r in rows:
            sum_d[r[0]] = r[1:]

    # read summary table from gdb
    summary_fields =  ['PIN', 'OWNER_CODE', 'OWNER', 'ASSESSED_ACRES', 'TOT_BENEFIT',
                       'TOT_ASSESSMENT', 'SECTION', 'TOWNSHIP', 'RANGE', 'COUNTY']

    # generate flags
    flagCount = 0
    flag_pins = []
    pin_error_msg = 'PIN not found in Breakdown Table'
    with utils.InsertCursor(gdb.flag_table, [f[0] for f in FLAG_FIELDS[:-1]]) as irows:
        with arcpy.da.SearchCursor(gdb.summary_table, summary_fields) as rows:
            for r in rows:
                newRow = [None] * len(FLAG_FIELDS[:-1])
                par = None
                if r[0] in sum_d:
                    plss = '-'.join(['{:0>2}'.format(p) if p else '99' for p in r[6:9]])
                    par = sum_d[r[0]]
                    newRow[0] = r[0]

                    # check owner code
                    if r[1] != par[0]:
                        newRow[2] = 'Owner Code "{}" does not macth "{}" in breakdown table"'.format(r[1] if r[1] else '', par[0] if par[0] else '')
                    own = r[2]

                    # check owner last name only
                    if own and par[1]:
                        ownLast = own.split()[0].upper().rstrip(',')
                        bownLast = par[1].split()[0].upper().rstrip(',')
                        if ownLast != bownLast:
                            newRow[3] = 'Last name "{}" in summary table does not match "{}" in breakdown table'.format(ownLast, bownLast)

                    # check acres based on pecent threshold
                    acres = r[3]
                    bacres = par[2]
                    diff = acres - bacres
                    perc_diff = (acres * acre_threshold)

                    if abs(diff) >= perc_diff and abs(diff) >= min_acre_diff:
                        newRow[4] = diff
                        newRow[5] = perc_diff

                    # check benefits and assessments, these should be exact matches!
                    ben_diff = r[4] - par[3]
                    if ben_diff:
                        if ben_diff > 0.1:
                            newRow[6] = ben_diff

                    assess_diff = r[5] - par[4]
                    if assess_diff:
                        if assess_diff > 0.1:
                            newRow[7] = assess_diff

                    # verify plss info
                    if plss != par[5]:
                        newRow[8] = 'Section "{}" does not match "{}" from breakdown table'.format(plss, par[5])

                else:
                    newRow[:2] = [r[0], pin_error_msg]

                if len(filter(None, newRow)) >= 2:
                    # add county
                    newRow[9] = r[-1]
                    irows.insertRow(newRow)
                    flagCount += 1

                    if newRow[1] != pin_error_msg:
                        flag_pins.append(newRow[0])

    # flag PINs in breakdown table, PINs keep getting set to NULL from relationship table??
    with utils.UpdateCursor(gdb.breakdown_table, [utils.PIN, 'FLAG']) as urows:
        for row in urows:
            if row[0] in flag_pins:
                row[1] = 'Y'
            else:
                row[1] = 'N'
            urows.updateRow(row)

    # flag PINs in summary table
    with utils.UpdateCursor(gdb.summary_table, [utils.PIN, 'FLAG']) as rows:
        for row in urows:
            if row[0] in flag_pins:
                row[1] = 'Y'
            else:
                row[1] = 'N'
            rows.updateRow(row)

##    # set up relationship classes, this is killing GDB performance, will just have to go with table joins :(
##    sum_rel = os.path.join(gdb.path, 'Summary_Relationship')
##    brk_rel = os.path.join(gdb.path, 'Breakdown_Relationship')
##    if not arcpy.Exists(sum_rel):
##        arcpy.management.CreateRelationshipClass(gdb.summary_table, gdb.flag_table, sum_rel, 'SIMPLE', 'Flags', 'Summary', 'BOTH', 'ONE_TO_ONE', 'NONE','PIN', 'PIN')
##        utils.Message('created ' + os.path.basename(sum_rel))
##
##    if not arcpy.Exists(brk_rel):
##        arcpy.management.CreateRelationshipClass(gdb.flag_table, gdb.breakdown_table, brk_rel, 'SIMPLE', 'Breakdown', 'Flags', 'BOTH', 'ONE_TO_MANY', 'NONE', 'PIN', 'PIN')
##        utils.Message('created ' + os.path.basename(brk_rel))

    # compact gdb
    arcpy.management.Compact(gdb.path)

    # report message
    utils.Message('Found {} flags between summary and breakdown tables'.format(flagCount))
    return