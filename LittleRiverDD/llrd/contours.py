#-------------------------------------------------------------------------------
# Name:        contours
# Purpose:     generate clean contours, especially in areas with low relief
#
# Author:      Caleb Mackey
#
# Created:     05/06/2016
# Copyright:   (c) calebma 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
arcpy.env.overwriteOutput = True

def getContours(dem, out_contours, interval=2, z_factor=3.28084, index_interval=10, contour_length_threshold=200):
    """generates clean contours, especially in areas with low relief.  Smooths the
    raster with focal statistics first.

    Required:
        dem -- input DEM
        out_contours -- output contours

    Optional:
        interval -- contour interval, default is 2ft
        z_factor -- option to apply a Z-factor, use 3.2084 if the DEM Z values are in
            meters, use 1 if already in feet.
        index_interval -- in the 'CONTOUR_TY' field, contours divisible by this value
            will recieve a value of 'INDEX', while all others will be 'INTERMEDIATE'.
            This is helpful for displaying contours at evey 10 ft differently than
            all the others.  Default is 10.

        contour_length_threshold -- a minimum contour length can be specified to remove any
            closed polylines for very smal areas.  All contours with a length less than this
            value will be removed.
    """
    interval = int(interval)
    z_factor = float(z_factor)
    index_interval = int(index_interval)
    contour_length_threshold = int(contour_length_threshold)

    # check out spatial analyst license if available
    if arcpy.CheckExtension('Spatial').lower() == 'available':
        arcpy.CheckOutExtension('Spatial')

    else:
        raise NotImplementedError('Spatial Analyst is not available!')

    # smooth raster
    smooth = r'in_memory\smooth' #os.path.join(arcpy.env.scratchWorkspace, 'tmp_smooth')
    arcpy.env.cellSize = 3
    nbCir = arcpy.sa.NbrCircle(3, 'CELL')
    tmp = arcpy.sa.FocalStatistics(dem, nbCir, 'MEAN')
    tmp.save(smooth)

    # generate contours
    arcpy.sa.Contour(smooth, out_contours, interval, z_factor=z_factor)

    # add 'CONTOUR_TY' field and calculate
    arcpy.management.AddField(out_contours, 'CONTOUR_TY', 'TEXT')
    with arcpy.da.UpdateCursor(out_contours, ['Contour', 'CONTOUR_TY', 'SHAPE@LENGTH']) as rows:
        for r in rows:
            if r[0] % index_interval == 0:
                r[1] = 'Index'
            else:
                r[1] = 'Intermediate'
            if r[2] >= contour_length_threshold:
                rows.updateRow(r)
            else:
                rows.deleteRow()


    # check in license
    arcpy.CheckInExtension('Spatial')
    try:
        arcpy.management.Delete(smooth)
    except:
        pass

    return out_contours
