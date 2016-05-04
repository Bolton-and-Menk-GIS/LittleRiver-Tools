#-------------------------------------------------------------------------------
# Name:        Download
# Purpose:     Little River Drainage District Utilites
#
# Author:      Caleb Mackey
#
# Created:     02/25/2016
# Copyright:   (c) Bolton & Menk, Inc. 2016
#-------------------------------------------------------------------------------
from . import utils
import tempfile
import ftplib
import shutil
from auth import authenticate, _c_
import arcpy
import os
import glob

arcpy.env.overwriteOutput = True

##@utils.passArgs
@utils.timeit
def parcelDownload():
    """downloads parcels from counties from FTP site and updates them in
    Littel River Geodatabase"""

    # access FTP
    theDir = '/LittleRiverCounties'

    try:
        ftp = ftplib.FTP()
        _c_(ftp)
        authenticate(ftp)

        # zip parcels
        tmpdir = tempfile.mkdtemp()
        #desktop = os.path.expanduser(os.sep.join(['~', 'Desktop']))
        #tmpdir = os.path.join(desktop, 'Parcel_Download')
        if not os.path.exists(tmpdir):
            os.makedirs(tmpdir)
        print tmpdir

        # llrd GDB
        gdb = utils.Geodatabase()

        # check if directory arleady exists
        ftp.cwd(theDir)
        zips = ftp.nlst()

        # iterate through zips and unzip to temp dir
        for z in zips:
            print z

            dl_zip = os.path.join(tmpdir, z)
            ftp.retrbinary('RETR {}'.format(z), open(dl_zip, 'wb').write)
            utils.Message('Downloaded: "{}"'.format(z))

            # unzip it
            utils.unzip(dl_zip)
            os.remove(dl_zip)

        # quite session
        ftp.quit()

        # append files
        folders = os.listdir(tmpdir)
        print folders
        for folderName in folders:
            print folderName
            folder = os.path.join(tmpdir, folderName)
            parConfigFile = os.path.join(folder, 'parcelConfig.json')
            pConfig = utils.getParcelConfig(parConfigFile)
            parcels = os.path.join(tmpdir, folderName, folderName + '_PARCELS.shp')

            # get field_map dict
            field_map = utils.getFieldMapDict(parConfigFile)
            gdb_pars = gdb.getParcelPath(pConfig.county, 'county')
            fmap = utils.fieldMappings([gdb_pars, parcels], field_map)

            # do update
            gdb.updateParcels(parcels, pConfig.county, fmap)

            # clean up
            arcpy.management.Delete(parcels) # delete this first in case of schema locks
            os.remove(parConfigFile)

            shutil.rmtree(folder)

        # compact database
        arcpy.management.Compact(gdb.path)

    except Exception as e:
        raise e

    finally:
        try:
            shutil.rmtree(tmpdir)
        except:
            pass
        return
