#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
copyright xiaofan.wxf
'''

import re
import sys
import os
import StringIO

reload(sys)
sys.setdefaultencoding('utf-8')

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'],'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient, View
import com.dtmilano.android.adb.adbclient
import com.dtmilano.android.viewclient
from viewHelper import *

class DeviceModify():
    def __init__(self):
        self.device = None
        self.serialno = None
        self.vc = None
        self.openapp()
        
    def openapp(self):
        self.device,self.serialno = ViewClient.connectToDeviceOrExit()

        FLAG_ACTIVITY_NEW_TASK = 0x10000000
        componentName = 'com.example.myxposed/.ParamActivity'

        self.device.startActivity(component=componentName,flags=FLAG_ACTIVITY_NEW_TASK)
        ViewClient.sleep(2)
        self.vc = ViewClient(self.device,self.serialno,forceviewserveruse=True)

    def modifyRandom(self):
        waitViewById('id/imei',self.vc)
        self.vc.findViewById('id/button2').touch()
        self.vc.dump()
        deviceIMEI = self.vc.findViewById('id/imei').getText()
        deviceIMSI = self.vc.findViewById('id/subscriberId').getText()
        
        f = open('device_imei.txt','w+')
        try:
            print 'save imei %s to file device_imei.txt'%(deviceIMEI)
            f.writelines(deviceIMEI +"\t"+deviceIMSI)
        finally:
            if(f != None):
               f.close() 

    def modify2IMEI(self,imei,imsi=None):
        waitViewById('id/imei',self.vc)
        self.vc.dump()
        #print 'imei is ',imei
        self.vc.findViewById('id/imei').setText(imei[0:15])
        #if imsi != None:
        #    self.vc.findViewById('id/subscriberId').setText(imsi[0:15])
        self.vc.findViewById('id/button1').touch()


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print 'Usage: python device_modify.py random/imei imsi'
        exit()

    imei = sys.argv.pop(1)
    if(imei == 'random'):
        DeviceModify().modifyRandom()
    elif(len(sys.argv) == 1):
        DeviceModify().modify2IMEI(imei)
    else:
        imsi = sys.argv.pop(1)
        DeviceModify().modify2IMEI(imei,imsi)
