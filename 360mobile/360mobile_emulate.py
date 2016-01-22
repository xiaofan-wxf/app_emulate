#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
copyright xiaofan.wxf
'''

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'],'src'))
except:
    pass
import re
import sys
import os
import time
import StringIO
sys.path.append("..")
from viewHelper import *
from com.dtmilano.android.viewclient import ViewClient, View
import com.dtmilano.android.adb.adbclient
import com.dtmilano.android.viewclient

reload(sys)
sys.setdefaultencoding('utf-8')

class NineGameEmulate():
    def __init__(self):
        self.device = None
        self.serialno = None
        self.vc = None
        self.accountfilename = '360mobile_imei_list.'+time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def openapp(self):
        self.device,self.serialno = ViewClient.connectToDeviceOrExit(serialno=None)

        FLAG_ACTIVITY_NEW_TASK = 0x10000000
        componentName = 'com.qihoo.browser/.activity.SplashActivity'
        self.device.startActivity(component=componentName,flags=FLAG_ACTIVITY_NEW_TASK)
        ViewClient.sleep(3)
        self.vc = ViewClient(self.device,self.serialno,forceviewserveruse=True)

    def doSomeClick(self,imei,imsi=None):
        if self.device == None :
            self.openapp()

        self.device.dragDip((400,400),(10,400),800,5)
        ViewClient.sleep(3)
        self.device.dragDip((400,400),(10,400),800,5)
        ViewClient.sleep(3)
        #waitViewByTx('立即修复',self.vc)
        #self.vc.findViewWithText('立即修复').touch()

        #ViewClient.sleep(10)
	self.device.touch(300,300,2)
	self.device.touch(300,500,2)

        f = open(self.accountfilename,'a')
        try:
            f.writelines(imei+"\t"+imsi+"\r\n")
        finally:
            f.flush()
            f.close()
    
    def reactiveMobile(self):
        if self.device == None :
            self.openapp()

        waitViewById('id/rgBottomNav',self.vc)
        self.device.touch(675,95,2)

        ViewClient.sleep(3)
        self.vc.findViewById('id/game_name').touch()
        
if __name__=='__main__':
    optype = sys.argv.pop(1)
    if optype == 'reactive':
       NineGameEmulate().reactiveMobile() 
    else:
       NineGameEmulate().doSomeClick(sys.argv.pop(1),sys.argv.pop(1))
