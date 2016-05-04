import sys
import os

try:
    imp_dir = os.path.dirname(os.path.dirname(__file__))
except:
    imp_dir = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))

# custom library
sys.path.append(imp_dir)
from llrd import proxy, utils

# test args
args = [r'\\ArcServer1\GIS\KLINGNER_PR\X11111474\ESRI\Tools\misc\proxyTest', 'Scott']
landowners = utils.passArgs(proxy.generateProxyBallots, args)
