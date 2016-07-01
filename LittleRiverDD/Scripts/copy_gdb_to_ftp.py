import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from llrd import utils
import tempfile
import ftplib
import shutil
import time
from llrd.auth import authenticate, _c_

# access FTP
theDir = '/Klingner'
stamp = time.strftime('_%Y%m%d%H%M%S')

ftp = ftplib.FTP()
_c_(ftp)
authenticate(ftp)

try:
    gdb = utils.getConfig().get('Geodatabase', '')

    if os.path.exists(gdb):
        zip_name = './gdb_backups/' + os.path.splitext(os.path.basename(gdb))[0] +  stamp
        data = open(shutil.make_archive(zip_name, 'zip', gdb), 'rb')
        subFile = '{}/{}.zip'.format(theDir, zip_name)
        ftp.storbinary('STOR {}'.format(subFile), data)
        data.close()
        utils.Message('Successfully Uploaded "{}.zip" to FTP Site'.format(zip_name))

finally:
    ftp.quit()
