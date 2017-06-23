#!/usr/bin/python

import os
import sys

#apache
APACHE_DATA = "httpd.txt"
os.chdir(os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(__file__))

#supplies:
# 1 - csvFileName
# 2 - adminEmail

# 3 - clusterName
# 4 - devMode (True|1 / False|0)

from webappSrc import *

from httpd import *

csvInit(csvFilename)
smtpInit(adminEmail)

setClusterName(clusterName)
setDevMode(devMode)
 
application = default_app()

