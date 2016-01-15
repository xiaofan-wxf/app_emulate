#!/usr/bin/python
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

class LeHaiEmulate():
    def __init__(self):
        self.device = None
        self.serialno = None
        self.vc = None
        self.accountfilename = 'lehai_imei_list.'+time.strftime('%Y-%m-%d',time.localtime(time.time()))

    def openapp(self):
        self.device,self.serialno = ViewClient.connectToDeviceOrExit(serialno=None)

        FLAG_ACTIVITY_NEW_TASK = 0x10000000
        componentName = 'com.lehai.ui/com.showself.ui.LoadingActivity'
        self.device.startActivity(component=componentName,flags=FLAG_ACTIVITY_NEW_TASK)
        ViewClient.sleep(3)
        self.vc = ViewClient(self.device,self.serialno,forceviewserveruse=True)

    def activeMobile(self,imei,imsi=None):
        if self.device == None :
            self.openapp()

        waitViewById('id/quick_guide_viewpager',self.vc)
        self.device.dragDip((500,300),(30,300),200,2)

	self.vc.dump()
	self.device.touch(615,378,2)	

	waitViewById('id/home_bottom_tab5',self.vc)
	self.vc.findViewById('id/home_bottom_tab5').touch()

	self.vc.dump()
	waitViewById('id/btn_login_note_left',self.vc)
	#self.vc.findViewById('id/btn_login_note_left').touch()
	self.device.touch(160,1188,2)

	self.vc.dump()
	waitViewByTx('乐嗨号注册',self.vc)
	self.vc.findViewWithText('乐嗨号注册').touch()
	
	self.vc.dump()
	name = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(5)))
	self.vc.findViewById('id/et_lehai_reg_account').setText(name)
	self.vc.findViewById('id/et_reg_password').setText('abc1234')
	self.vc.findViewById('id/btn_lehai_reg').touch()

	self.vc.dump()
	waitViewById('id/btn_register_finish',self.vc)
	self.vc.findViewById('id/btn_register_finish').touch()

	self.vc.dump()
        waitViewById('id/imageView_classify_more_recommend',self.vc)
        self.vc.findViewById('id/imageView_classify_more_recommend').touch()
        ViewClient.sleep(5)
        
        f = open(self.accountfilename,'a')
        try:
            f.writelines(name+"\t"+imei+"\t"+imsi+"\r\n")
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
       LeHaiEmulate().reactiveMobile() 
    else:
       LeHaiEmulate().activeMobile(sys.argv.pop(1),sys.argv.pop(1))
