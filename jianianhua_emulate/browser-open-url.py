#! /usr/bin/env python
'''
Copyright (C) 2012  Diego Torres Milano
Created on Mar 13, 2012

@author: diego
'''


import re
import sys
import os
import string

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient

USE_BROWSER = True
# Starting: Intent { act=android.intent.action.MAIN flg=0x10000000 cmp=com.android.browser/.BrowserActivity }
if USE_BROWSER:
    #package = 'com.android.browser'
    package = 'com.android.browser'
    activity = '.BrowserActivity'
else:
    package = 'com.android.chrome'
    activity = 'com.google.android.apps.chrome.Main'
component = package + "/" + activity
#uri = 'https://res.imtt.qq.com/schoolcode/html/index.html?ADTAG=hbxy2'
uri = 'https://res.imtt.qq.com/schoolcode/html/index.html?ADTAG=hbkp'

device, serialno = ViewClient.connectToDeviceOrExit(serialno=sys.argv.pop(1))
device.startActivity(component=component, uri=uri)

ViewClient.sleep(6)
device.touch(300,800)
ViewClient.sleep(4)
