import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'],'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient

def waitViewById(viewId,vc):
    #while True:
    for i in range(20):
        vc.dump()
        if vc.findViewById(viewId):
            print 'view with id %s is appeared----'%(viewId)
            break
        else:
            print 'view with id %s not appear wait 1 second for a while------'%(viewId)
            ViewClient.sleep(3)

def waitViewByTx(text,vc):
    #while True:
    for i in range(20):
        vc.dump()
        if vc.findViewWithText(text):
            print 'view with text %s is appeared----'%(text)
            break
        else:
            print 'view with text %s not appear wait 1 second for a while------'%(text)
            ViewClient.sleep(3)
