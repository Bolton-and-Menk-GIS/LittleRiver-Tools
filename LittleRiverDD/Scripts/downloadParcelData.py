import sys
import os

try:
    imp_dir = os.path.dirname(os.path.dirname(__file__))
except:
    imp_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))

# custom library
sys.path.append(imp_dir)
from llrd import download, utils
reload(download)

# download and update all parcels
##utils.passArgs(download.parcelDownload, [])
download.parcelDownload()
