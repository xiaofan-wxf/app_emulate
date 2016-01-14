# !/usr/bin/python
# -*- coding: utf-8 -*-
import os,httplib,socket,urllib2,urllib,json,cookielib
import ConfigParser
import MultipartPostHandler
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

class LianZHongDaMa() :
    def __init__(self):
        self.USERNAME=""    # 用户名名
        self.PASSWD=""      # 密码
        self.INIFILEPATH="" # ini文件路径
        self.WORKER=""      # 打码人
        self.TOKEN=""       # token

    def GetLianZHong_UserPass(self,iniPath=None):  #读取INI,获取用户名，密码
        """
        config.ini文件格式如下：
        [LianZHong]
        Username=用户名
        Password=密码

        """
        if iniPath==None:
            self.INIFILEPATH=os.getcwd() +"/config.ini"
        else:
            self.INIFILEPATH=iniPath
        try:
            config = ConfigParser.ConfigParser()
            config.readfp(open(self.INIFILEPATH)) #读取当前目录下的ini文件
            self.USERNAME = config.get("LianZHong","Username")
            self.PASSWD   = config.get("LianZHong","Password")
            self.TOKEN = config.get("LianZHong","Token")
        except Exception, e:
            print "读取INI错误,不能自动打码，请配置config.ini文件,异常代码：\n",str(e)
        finally:
            # print ("Username:", self.USERNAME)
            # print ("Password",self.PASSWD)
            pass


    def sendPicture(self,imgpath):
        """
            提交验证码图片
        """        
        socket.setdefaulttimeout(60)
        if self.USERNAME=="" or self.PASSWD=="":
            self.GetLianZHong_UserPass()
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler.MultipartPostHandler)
        params = {  "info[lz_user]" : self.USERNAME,
                    "info[lz_pass]" : self.PASSWD,
                    "imagepath"     : open(imgpath, "rb"),
                    'pesubmit'      :''
                    }

        tmp=None
        code=None
        ret=["",""]
        try:
            tmp=opener.open("http://bbb4.hyslt.com/api.php?mod=php&act=upload", params).read()

            #code=re.findall("window.location.href='http://fsdm3.yzmbuy.com/index.php/demo/(\d+)'",tmp)[0]
            # print code
        except Exception, e:
            print str( e)
            return ret


        url="http://fsdm3.yzmbuy.com/index.php?mod=demo&act=result&id=%s"%code

        retry=0
        while retry<10:
            retry+=1
            print('等待返回打码结果...')
            time.sleep(3)
            try:
                result=opener.open(url).read().split("<")[0]
                res = json.loads(result)
                if res['result']!=None:
                    print('result:%s,worker:%s'%(res['result'],res['damaworker']))
                    ret[0]=res['result'].encode("utf-8")
                    ret[1]=res['damaworker'].encode("utf-8")
                    self.WORKER=res['damaworker'].encode("utf-8")
                    break
            except  Exception, e:
                print ("自动打码出错了,错误代码",str(e))
                pass

        if len(ret[0]) <3:
            print ("自动打码超时没有响应...")

        return ret

    def reportError(self):
        """
            报告打码错误
        """
        print ("报告打码错误参数%s:%s" %(self.WORKER,self.USERNAME))
        data=urllib.urlencode({"worker":self.WORKER , "username": self.USERNAME ,"submit":"添 加"})
        socket.setdefaulttimeout(60)
        print data
        ret=0
        conn = httplib.HTTPConnection("dama3.yzmbuy.com" + ':' + "80")
        headers = { "Host" :  "dama3.yzmbuy.com" ,
                    "User-Agent" :  r'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)' ,
                    "Connection": "Keep-Alive",
                    "Accept-Language": "en-US",
                    "Connection":"Keep-Alive",
                    "Cache-Control":"no-cache",
                    "Referer":r'http://dama3.yzmbuy.com/lz_yzmphp/update_err.php',
                    "Origin":r'http://dama3.yzmbuy.com',
                    "Content-Type": r'application/x-www-form-urlencoded',
                    "Accept-Encoding":"gzip, deflate",
                    "Accept": "text/html, application/xhtml+xml, */*",
                    "Content-Length": len(data)
                    }
        try:
            conn.request("POST", r"/lz_yzmphp/update_err.php", data,headers)
            rs = conn.getresponse()
            if rs.status==200:
                ret=1
        except Exception, e:
            print('reportError no response ...Error code:',str(e))
            conn.close()
        finally:
            if conn!=None:
                conn.close()
        return ret
      
    def getLeftPoint(self):
        """
            获取剩余点数
        """
        
        data=urllib.urlencode({"user_name":self.USERNAME , "user_pw": self.PASSWD})
        socket.setdefaulttimeout(60)
        # print data
        ret=-1
        #conn = httplib.HTTPConnection("dama3.yzmbuy.com" + ':' + "80")
       # headers = { "Host" :  "bbb4.hyslt.com" ,
       #             "User-Agent" :  r'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)' ,
       #             "Connection": "Keep-Alive",
       #             "Accept-Language": "en-US",
       #             "Connection":"Keep-Alive",
       #             "Cache-Control":"no-cache",
       #             "Referer":r'http://bbb4.hyslt.com/api.php',                    
       #             "Content-Type": r'application/x-www-form-urlencoded',
       #             "Accept-Encoding":"gzip, deflate",
       #             "Accept": "text/html, application/xhtml+xml, */*",
       #             "Content-Length": len(data)
       #             }
        #request = urllib2.Request(r'http://dama3.yzmbuy.com:80/lz_yzmphp/GetInfo.php',data=data,headers=headers)
#headers=headers
        request = urllib2.Request('http://bbb4.hyslt.com/api.php?mod=php&act=point',data=data)
        
        try:
            #conn.request("POST", r'/lz_yzmphp/GetInfo.php', data,headers)
            res= urllib2.urlopen(request)
            #rs = conn.getcode()
            if res.getcode()==200:
                return res.read()
                #w=body.find(":")
                #if w==-1:
                #    ret=-1
                #body=body[w+len(":"):]  
                #w=body.find("\r\n")
                #if w==-1:
                #    ret=-1
                #body=body[:w]    
                ## print body
                #ret=int(body)                     
        except Exception, e:
            print('getLeftPoint no response ...Error code:',str(e))          
        finally:
            if res!=None:
                res.close()
        #return ret


    def uploadImage(self,imagepath):
       """
           提交验证码图片
       """        
       socket.setdefaulttimeout(60)
       if self.USERNAME=="" or self.PASSWD=="":
           self.GetLianZHong_UserPass()

       #cookies = cookielib.CookieJar()
       #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler.MultipartPostHandler)
       register_openers()

       datagen,headers = multipart_encode({'user_name':self.USERNAME,
                                           'user_pw':self.PASSWD,
                                           'yzm_minlen':4,
                                           'yzm_maxlen':4,
                                           'yzm_type_mark':0,
                                           'zztool_token':self.TOKEN,
                                           'upload':open(imagepath,'rb')})

       #data = urllib.urlencode({'user_name':self.USERNAME,
       #                         'user_pw':self.PASSWD,
       #                         'yzm_minlen':4,
       #                         'yzm_maxlen':4,
       #                         'yzm_type_mark':0,
       #                         'zztool_token':self.TOKEN,
       #                         'upload':open(imagepath,'rb')})

       # headers = { "Host" :  "bbb4.hyslt.com" ,
       #             "User-Agent" :  r'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)' ,
       #             "Connection": "Keep-Alive",
       #             "Accept-Language": "en-US",
       #             "Connection":"Keep-Alive",
       #             "Cache-Control":"no-cache",
       #             "Referer":r'http://bbb4.hyslt.com/api.php',                    
       #             "Content-Type": r'application/x-www-form-urlencoded',
       #             "Accept-Encoding":"gzip, deflate",
       #             "Accept": "text/html, application/xhtml+xml, */*",
       #             "Content-Length": len(data)
       #             }
       request = urllib2.Request('http://bbb4.hyslt.com/api.php?mod=php&act=upload',datagen,headers)
       try:
           res= urllib2.urlopen(request)
           #res = opener.open("http://bbb4.hyslt.com/api.php?mod=php&act=upload", data)
           print 'upload image response code is '+str(res.getcode())
           if res.getcode()==200:
               return res.read().split("<")[0]
       except Exception, e:
           print('upload image no response ...Error code:',str(e))          
       finally:
           if res!=None:
               res.close()


if __name__ == '__main__':
    lz=LianZHongDaMa()
    print lz.uploadImage('verifycode.png')
    #lz.GetLianZHong_UserPass()
    #print lz.getLeftPoint()
    
