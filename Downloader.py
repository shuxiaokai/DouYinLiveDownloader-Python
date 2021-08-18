#-*- coding: utf-8 -*- 
import requests
import re
import os
#from six.moves import urllib
import urllib.request
import sys
from bs4 import BeautifulSoup
import time
import json
import configparser
# import socket
import subprocess
import logging
import threading

"""
2021年8月18日修复说明：
修改UA并修改获取直播间名称方式
"""

class Logger(object):

    def __init__(self, stream=sys.stdout):
        output_dir = "log"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # output_dir = "log\\"+ time.strftime('%Y-%m-%d')
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)    
        #log_name = '{}.log'.format(time.strftime('%Y-%m-%d-%H-%M'))
        #log_name = '{}.log'.format(time.strftime('%Y-%m-%d-%H-%M'))
        log_name = "崩溃记录日志.log"
        filename = os.path.join(output_dir, log_name)

        self.terminal = stream
        self.log = open(filename, 'w',encoding="utf-8-sig")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

sys.stdout = Logger(sys.stdout)  #  将输出记录到log
sys.stderr = Logger(sys.stderr)  # 将错误信息记录到log    
# 创建一个logger 
logger = logging.getLogger('抖音直播录制0517版')  
logger.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件 
if not os.path.exists("log"):
    os.makedirs("log")    
fh = logging.FileHandler("log/直播日志文件.log",encoding="utf-8-sig",mode="a")
fh.setLevel(logging.WARNING)

# 再创建一个handler，用于输出到控制台 
# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# formatter = logging.Formatter()
# ch.setFormatter(formatter)

# 定义handler的输出格式 
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
#ch.setFormatter(formatter)

# 给logger添加handler 
logger.addHandler(fh)
# logger.addHandler(ch)


# socket.setdefaulttimeout(10)




recording=[]


logger.warning("------------------------------------------------------") #分割线

def updateFile(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8-sig") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8-sig") as f:
        f.write(file_data)


def subwords(words):  
    words=re.sub('[? * : " < >  / |]', '', words) 
    words=re.sub(r'\\', '', words) 
    return words

    
def get_roomid(html):
    js = re.findall(r"<script>(.{666,}?)</script>", html)[0]
    ret = json.loads(js.replace("window.__INIT_PROPS__ = ",""))
    # if "own_room" in ret["/webcast/reflow/:id"]["room"]["owner"].keys():
    #print("ret:"+ret)
    return ret["/webcast/reflow/:id"]["room"]["owner"]["own_room"]["room_ids_str"][0]

def get_status(html):
    js = re.findall(r"<script>(.{666,}?)</script>", html)[0]
    ret = json.loads(js.replace("window.__INIT_PROPS__ = ",""))
    # if "own_room" in ret["/webcast/reflow/:id"]["room"]["owner"].keys():
    return ret["/webcast/reflow/:id"]["room"]["status"]


def get_real_url(rid,startname,changestaute):
    global recording
    #room_status=""
    
    try:
        #print('开始获取真实地址:')
        Modelheaders = {  
        #'upgrade-insecure-requests':'1',
        #'User-Agent':'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Nexus 6P Build/OPM7.181205.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.11.1.1197 Mobile Safari/537.36'
        'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/13.0 MQQBrowser/10.1.1 Mobile/15B87 Safari/604.1 QBWebViewUA/2 QBWebViewType/1 WKType/1'
        }

        if len(proxies2)>0:
            res=requests.get(rid,headers=Modelheaders,proxies=proxies2,timeout=15)
        else:
            res=requests.get(rid,headers=Modelheaders,timeout=15)
        #print(res.text)


        #print(res.text)
        # with open("statue2.txt","w",encoding="utf8") as f:        
        #     f.write(res.text)  # 自带文件关闭功能，不需要再写f.close()
        #room_status = str(get_status(res.text))
        
        # print("直播间状态: "+room_status)
        # if room_status=="2":
        #     pass            
        #     if changestaute!=room_status:
        #         changestaute=room_status
        #         logger.warning("直播间正在直播")
        #     else:
        #         print("直播间正在直播")

        # elif room_status=="4":
        #     pass
            
        #     if changestaute!=room_status:
        #         changestaute=room_status        
        #         logger.warning("直播间直播已结束,正在等待下次开播")
        #     else:
        #         print("直播间直播已结束,正在等待下次开播")
        # elif room_status=="1":
        #     pass
           
        #     if changestaute!=room_status:
        #         changestaute=room_status
        #         logger.warning("直播间未直播")
        #     else:                
        #         print("直播间未直播")
        # else:
            
        #     if changestaute!=room_status:
        #         changestaute=room_status
        #         logger.warning("未知状态.直播间状态返回码: "+room_status)
        #     else:                
        #         print("未知状态.直播间状态返回码: "+room_status)
        

        try:
            room_ids_str = get_roomid(res.text)
            changestautenow=True
        except:
            changestautenow=False

        #nowdate=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        nowdate=time.strftime("%H:%M:%S", time.localtime())
        if changestaute!=changestautenow:
            changestaute=changestautenow
            if changestautenow==True:
                logger.warning(startname+" 正在直播中 ")
                print("\r"+startname+" 正在直播 " + nowdate)
            else:
                
                logger.warning(startname+"  直播间未直播,等待开播中.. ")
                print(startname+"  直播间未直播,等待开播中.. "+nowdate)
                if startname in recording:
                     recording.remove(startname) 
        else:
            if changestautenow==True:
                print("\r"+startname+" 正在直播中 " +nowdate)
            else:
                print(startname+"  直播间未直播,等待开播中.. "+nowdate)
                if startname in recording:
                     recording.remove(startname) 


        room_url = 'https://webcast.amemv.com/webcast/reflow/{}'.format(room_ids_str)+"?u_code=70baflkg&app=aweme&utm_campaign=client_share&utm_medium=ios&tt_from=copy&utm_source=copy"
        
        
        Modelheaders = {  
        #'upgrade-insecure-requests':'1',
        'User-Agent':'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Nexus 6P Build/OPM7.181205.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.11.1.1197 Mobile Safari/537.36'
        }
        
        if len(proxies2)>0:
            res=requests.get(room_url,headers=Modelheaders,proxies=proxies2,timeout=15)
        else:
            res=requests.get(room_url,headers=Modelheaders,timeout=15)

        lenresult=len(res.text)    
        info=res.text[re.search("hls_pull_url",res.text).span()[0]:lenresult]
        result1=re.search("hls_pull_url\":\"",info).span()[1]
        result2=re.search("\",\"",info).span()[0]   
        hls_pull_url=info[result1:result2]
        #print("hls_pull_url: " +str(hls_pull_url))
        if videom3u8:
            print(startname + " 在线直播地址:" +str(hls_pull_url))

        info=res.text[re.search("rtmp_pull_url",res.text).span()[0]:lenresult]
        result1=re.search("rtmp_pull_url\":\"",info).span()[1]
        result2=re.search("\",\"",info).span()[0]   
        rtmp_pull_url=info[result1:result2]
        #print("rtmp_pull_url: "+str(rtmp_pull_url))

        
        #real_url=[rtmp_pull_url,room_status]
        real_url=[rtmp_pull_url,changestaute]
        return real_url
    except Exception as _e:
        # if room_status=="4":
        #     #print("直播间直播已结束,正在等待下次开播")
        #     real_url = [None,"4"]            
        # else:
        #     print("可能获取超时,反馈信息: "+str(e))
        #     real_url = [None,"0"]
        real_url = [None,changestaute]
        return real_url

# def _progress(block_num, block_size, total_size):
#             '''回调函数
#             @block_num: 已经下载的数据块
#             @block_size: 数据块的大小
#             @total_size: 远程文件的大小
#             '''
#             #sys.stdout.write('\r>> 正在录制 %s %.1f%%' % (filename,float(block_num * block_size) / float(total_size) * 100.0))
#             sys.stdout.write('\r>> 正在录制 %s %.1f%%' % (filename,float(block_num * block_size)/1000))
            
#             sys.stdout.flush() 


headers = {  
            'Referer':'https://www.baidu.com/',    
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            }


print( '-------------- 吾爱破解论坛 程序当前配置----------------' )   
print("循环值守录制抖音直播 版本:0517")

try:
  f =open("config.ini",'r', encoding='utf-8-sig')
  f.close()

except IOError:
  f = open("config.ini",'w', encoding='utf-8-sig')
  f.close()



try:
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    rid=config.get('1', '直播地址')
except:
    rid=""



if os.path.isfile("URL_config.ini"):    
    f =open("URL_config.ini",'r', encoding='utf-8-sig')
    inicontent=f.read()
    f.close()
else:
    inicontent=""







# rid=f.read()
# f.close()


if len(inicontent)==0:
    print('请输入要录制的抖音主播分享网址,例如: https://v.douyin.com/EQBYoH/:')
    inurl=input()
    f = open("URL_config.ini",'a+',encoding='utf-8-sig')
    f.write(inurl)
    f.close()
    
    config = configparser.ConfigParser()
    # -read读取ini文件

    config.read('config.ini', encoding='utf-8-sig')
    listx = []
    listx = config.sections()# 获取到配置文件中所有分组名称
    if '1' not in listx:# 如果分组type不存在则插入type分组
        config.add_section('1')

    else:
        config.remove_option('1', '直播地址')# 删除type分组的stuno
        # config.remove_section('tpye')# 删除配置文件中type分组

    #config.set('1', '直播地址', inurl)# 给type分组设置值
    config.set('1', '循环时间(秒)', '4')# 给type分组设置值

    o = open('config.ini', 'w',encoding='utf-8-sig')

    config.write(o)
    
    o.close()#不要忘记关闭


    
    
    #rid=inurl
    


try:
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    delaydefault=config.getint('1', '循环时间(秒)')
except:
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config.ini', encoding='utf-8-sig')
    listx = []
    listx = config.sections()# 获取到配置文件中所有分组名称
    if '1' not in listx:# 如果分组type不存在则插入type分组
        config.add_section('1')

    else:
        config.remove_option('1', '循环时间(秒)')# 删除type分组的stuno
        # config.remove_section('tpye')# 删除配置文件中type分组


    config.set('1', '循环时间(秒)', '4')# 给type分组设置值

    o = open('config.ini', 'w',encoding='utf-8-sig')

    config.write(o)
    
    o.close()#不要忘记关闭
    delaydefault=4


try:
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    videopath=config.get('1', '直播保存路径')
except:
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config.ini', encoding='utf-8-sig')
    listx = []
    listx = config.sections()# 获取到配置文件中所有分组名称
    if '1' not in listx:# 如果分组type不存在则插入type分组
        config.add_section('1')

    else:
        config.remove_option('1', '直播保存路径')# 删除type分组的stuno
        # config.remove_section('tpye')# 删除配置文件中type分组


    config.set('1', '直播保存路径', '')# 给type分组设置值

    o = open('config.ini', 'w',encoding='utf-8-sig')

    config.write(o)
    
    o.close()#不要忘记关闭
    videopath=""

if len(videopath)>0:
    if not os.path.exists(videopath):
        print("配置文件里,直播保存路径并不存在,请重新输入一个正确的路径.或留空表示当前目录,按回车退出")
        input("程序结束")
        os._exit(0)
    else:
        print("视频保存路径: "+videopath)
else:
    print("视频保存路径: 当前目录")



try:    
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    videosavetype=config.get('1', '视频保存格式TS或FLV或MP4')

except Exception as _e:
    
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config.ini', encoding='utf-8-sig')
    listx = []
    listx = config.sections()# 获取到配置文件中所有分组名称
    if '1' not in listx:# 如果分组type不存在则插入type分组
        config.add_section('1')

    else:
        config.remove_option('1', '视频保存格式TS或FLV或MP4')# 删除type分组的stuno
        # config.remove_section('tpye')# 删除配置文件中type分组


    config.set('1', '视频保存格式TS或FLV或MP4',"TS")# 给type分组设置值

    o = open('config.ini', 'w',encoding='utf-8-sig')

    config.write(o)
    
    o.close()#不要忘记关闭
    videosavetype="TS"


#是否显示直播地址
try:    
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    videom3u8=config.get('1', '是否显示直播地址')

except Exception as _e:
    
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config.ini', encoding='utf-8-sig')
    listx = []
    listx = config.sections()# 获取到配置文件中所有分组名称
    if '1' not in listx:# 如果分组type不存在则插入type分组
        config.add_section('1')

    else:
        config.remove_option('1', '是否显示直播地址')# 删除type分组的stuno
        # config.remove_section('tpye')# 删除配置文件中type分组


    config.set('1', '是否显示直播地址',"否")# 给type分组设置值

    o = open('config.ini', 'w',encoding='utf-8-sig')

    config.write(o)
    
    o.close()#不要忘记关闭
    videom3u8="否"    


if videom3u8=="是":
    videom3u8=True
else:
    videom3u8=False


#是否显示循环秒数
try:    
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    looptime=config.get('1', '是否显示循环秒数')

except Exception as _e:
    
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config.ini', encoding='utf-8-sig')
    listx = []
    listx = config.sections()# 获取到配置文件中所有分组名称
    if '1' not in listx:# 如果分组type不存在则插入type分组
        config.add_section('1')

    else:
        config.remove_option('1', '是否显示循环秒数')# 删除type分组的stuno
        # config.remove_section('tpye')# 删除配置文件中type分组


    config.set('1', '是否显示循环秒数',"否")# 给type分组设置值

    o = open('config.ini', 'w',encoding='utf-8-sig')

    config.write(o)
    
    o.close()#不要忘记关闭
    looptime="否"    


if looptime=="是":
    looptime=True
else:
    looptime=False



#这里是控制MP4是否转码
try:    
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    videoencode=config.get('1', 'MP4格式是否转码H264')

except Exception as _e:
    
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config.ini', encoding='utf-8-sig')
    listx = []
    listx = config.sections()# 获取到配置文件中所有分组名称
    if '1' not in listx:# 如果分组type不存在则插入type分组
        config.add_section('1')

    else:
        config.remove_option('1', 'MP4格式是否转码H264')# 删除type分组的stuno
        # config.remove_section('tpye')# 删除配置文件中type分组


    config.set('1', 'MP4格式是否转码H264',"否")# 给type分组设置值

    o = open('config.ini', 'w',encoding='utf-8-sig')

    config.write(o)
    
    o.close()#不要忘记关闭
    videoencode="否"    


if videoencode=="是":
    videoencode=True
else:
    videoencode=False




#这里是控制是否设置代理
try:    
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    proxies2=config.get('1', '本地代理端口')
    proxiesn=proxies2
    if len(proxies2)>0:   
        
        proxies2={'https': 'http://127.0.0.1:'+str(proxies2)}        
        print("检测到有设置代理地址为: "+'http://127.0.0.1:'+str(proxiesn))

except Exception as _e:
    
    config = configparser.ConfigParser()
    # -read读取ini文件
    config.read('config.ini', encoding='utf-8-sig')
    listx = []
    listx = config.sections()# 获取到配置文件中所有分组名称
    if '1' not in listx:# 如果分组type不存在则插入type分组
        config.add_section('1')

    else:
        config.remove_option('1', '本地代理端口')# 删除type分组的stuno
        # config.remove_section('tpye')# 删除配置文件中type分组


    config.set('1', '本地代理端口',"")# 给type分组设置值

    o = open('config.ini', 'w',encoding='utf-8-sig')

    config.write(o)
    
    o.close()#不要忘记关闭

    proxies2=""    









if len(videosavetype)>0:
    if videosavetype.upper()=="FLV":
        videosavetype="FLV"
        print("直播视频保存为FLV格式")
    elif videosavetype.upper()=="TS":
        videosavetype="TS"
        print("直播视频保存为TS格式")
    elif videosavetype.upper()=="MP4":
        videosavetype="MP4"
        print("直播视频保存为MP4格式")        
    else:
        videosavetype="TS"
        print("直播视频保存格式设置有问题,这次录制重置为默认的TS格式")
else:
    videosavetype="TS"
    print("直播视频保存为TS格式")

if videoencode==True and videosavetype=="MP4":
    print("转码设置:MP4实时转码H264")

if videoencode==False and videosavetype=="MP4":
    print("转码设置:MP4不进行转码")







allLive=[]   #全部的直播
allRecordingUrl=[]
print( '......................................................' ) 

def startgo(line):
    global allLive
    recordfinish=False
    counttime=time.time()
    global videopath

    ridcontent = line.split(',')
    rid=ridcontent[0]
    if len(ridcontent)>1:
        print("传入地址: "+ridcontent[0],ridcontent[1])
    else:
        print("传入地址: "+ridcontent[0])

    while True:
        
        try:
            
            if len(proxies2)>0:
                res=requests.get(rid,headers=headers,proxies=proxies2,timeout=15)
            else:
                res=requests.get(rid,headers=headers,timeout=15)

            if res.status_code!=200:
                print(res.status_code)
                #input('直播地址连接失败,请手动检测配置文件里的地址是否正常')
                print(rid+' 的直播地址连接失败,请手动检测配置文件里的地址是否正常')
            else:
                # print(res.current_url)
                res.encoding='utf-8-sig'
                resdata=BeautifulSoup(res.text,'html.parser')
                # outname=resdata.find('span',class_='nickname')
                startname=(resdata.find('p',class_='name-wrap')).text
                # startname=re.sub('@','',outname.text)
                # startname = startname.replace(" ","")
                startname=subwords(startname)

                

                
                if startname in allLive:
                    print("新增的地址: %s 已经存在,本条线程将会退出"%startname)
                    #print('rid:'+rid)
                    
                    #updateFile(r"URL_config.ini", rid, "#"+rid) #将"D:\zdz\"路径的myfile.txt文件把所有的zdz改为daziran
                    namelist.append(str(rid)+"|"+str("#"+rid))
                    exit(0)
                # else:
                #     #print("检测到抖音直播间: "+startname.strip())
                #     allLive.append(startname)

                if len(ridcontent)==1:
                    # print(ridcontent[1])
                    # print("主播:"+startname.strip())
                    
                    #updateFile(r"URL_config.ini", ridcontent[1], "主播:"+startname.strip()) #将"D:\zdz\"路径的myfile.txt文件把所有的zdz改为daziran
                
                    namelist.append(str(ridcontent[0])+"|"+str(ridcontent[0]+",主播: "+startname.strip()))
                    #updateFile(r"URL_config.ini", ridcontent[0], ridcontent[0]+",主播: "+startname.strip()) #将"D:\zdz\"路径的myfile.txt文件把所有的zdz改为daziran
                # config = configparser.ConfigParser()
                # # -read读取ini文件
                # config.read('config.ini', encoding='utf-8-sig')
                # list = []
                # list = config.sections()# 获取到配置文件中所有分组名称
                # if '1' not in list:# 如果分组type不存在则插入type分组
                #     config.add_section('1')

                # else:
                #     config.remove_option('1', '主播')# 删除type分组的stuno
                #     # config.remove_section('tpye')# 删除配置文件中type分组

                # config.set('1', '主播', startname)# 给type分组设置值

                # o = open('config.ini', 'w',encoding='utf-8-sig')

                # config.write(o)
                
                # o.close()#不要忘记关闭

                break
                
        except Exception as e:    
            print("错误信息644:"+str(e)+"\r\n读取的地址为: "+str(rid))
            #input('直播地址连接失败,请手动检测配置文件里的地址是否正常--requests获取配置文件崩了')
            #print("读取的地址为:",str(rid))
            print(rid+' 的直播地址连接失败,请检测这个地址是否正常,可以重启本程序--requests获取失败')
            




        x=delaydefault
        #print('\r循环等待%d秒 '%x )
        #print('\r循环等待%d秒 '%x ,end="")
        if recordfinish==True:   
            counttimeend=time.time()-counttime
            if counttimeend<60:
                x=2
            else:
                recordfinish=False
        else:
            x=delaydefault


        while x:
            x = x-1
            #logger.debug('\r循环等待%d秒 '%x )
            if looptime:
                print('\r循环等待%d秒 '%x ,end="")
            time.sleep(1)
        if looptime:
            print('\r重新检测直播间中...',end="")
        

    changestaute=""
    while True:
        
        

        real_urlcontent = get_real_url(rid,startname,changestaute)

        real_url=real_urlcontent[0]
        changestaute=real_urlcontent[1]
        if real_url!=None:    
            
            #rid='https://v.douyin.com/EQBYoH/'
            #rid = input('请输入抖音直播间room_id或分享链接(例如: https://v.douyin.com/EQBYoH/): \n')
            #input('请在Config.ini配置文件里存入主播地址后,在这里继续')
            now = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())) 
            

            #print('如果要结束录制,请直接关闭本窗口!或者连续按两次Ctrl+C !')      


            
            try:
                if len(videopath)>0:
                    if videopath[-1]!="\\":
                        videopath=videopath+"\\"
                    if not os.path.exists(videopath+startname):
                    #创建路径                    
                        os.makedirs(videopath+startname)  
                else:
                    if not os.path.exists(startname):
                    #创建路径                    
                        os.makedirs('./'+startname)  

            except Exception as e:
                print("路径错误信息708: "+str(e))
            

            if not os.path.exists(videopath+startname):
                print("保存路径不存在,不能生成录制.请避免把本程序放在c盘,桌面,下载文件夹,qq默认传输目录.请重新检查设置")
                videopath=""
                print("因为配置文件的路径错误,本次录制在程序目录")
                        
            
            if videosavetype=="FLV":
                filename=startname + '_' + now + '.flv'         
                if len(videopath)==0:
                    print("\r"+startname+" 录制视频中: "+os.getcwd()+"\\"+startname +'\\'+ filename)
                else:
                    print("\r"+startname+" 录制视频中: "+videopath+startname +'\\'+ filename)

                if not os.path.exists(videopath+startname):
                    print("目录均不能生成文件,不能生成录制.请避免把本程序放在c盘,桌面,下载文件夹,qq默认传输目录.请重新检查设置,程序将会退出")
                    input("请按回车退出")
                    os._exit(0)
                #flv录制格式


                try:
                    recording.append(startname)
                    

                    #_filepath, _ = urllib.request.urlretrieve(rtmp_pull_url, videopath+startname +'\\'+ filename)
                    _filepath, _ = urllib.request.urlretrieve(real_url, videopath+startname +'\\'+ filename)
                    print('\n'+startname+" "+ time.strftime('%Y-%m-%d %H:%M:%S  ') + '直播录制完成\n')
                    logger.warning(startname+" "+"直播录制完成")
                    recordfinish=True
                    counttime=time.time()   
                    if startname in recording:
                        recording.remove(startname)                  

                except:
                    print('\r'+time.strftime('%Y-%m-%d %H:%M:%S  ') +startname + ' 未开播')      

            elif videosavetype=="MP4":            
                filename=startname + '_' + now + ".mp4"
                if len(videopath)==0:
                    print("\r"+startname+ " 录制视频中: "+os.getcwd()+"\\"+startname +'\\'+ filename)
                else:
                    print("\r"+startname+ " 录制视频中: "+videopath+startname +'\\'+ filename)

                ffmpeg_path = "ffmpeg"         
                file = videopath+startname +'\\'+ filename
                try:
                    recording.append(startname)
                    if videoencode:
                        _output = subprocess.check_output([
                            ffmpeg_path, "-y",
                            "-v","verbose", 
                            "-timeout","10000000", # 10s
                            "-loglevel","error",
                            "-hide_banner",
                            "-user_agent",headers["User-Agent"],
                            "-analyzeduration","2147483647",
                            "-probesize","2147483647",
                            "-i",real_url,
                            '-bufsize','5000k',
                            "-map","0",
                            "-sn","-dn",
                            # "-f","mpegts",
                            # "-bsf:v","h264_mp4toannexb",
                            # "-c","copy",
                            "-c:v","libx264",   #后期可以用crf来控制大小
                            #"-c:v","copy",   #直接用copy的话体积特别大.
                            '-max_muxing_queue_size','64',
                            "{path}".format(path=file),
                        ], stderr = subprocess.STDOUT)
                    else:
                        _output = subprocess.check_output([
                            ffmpeg_path, "-y",
                            "-v","verbose", 
                            "-timeout","10000000", # 10s
                            "-loglevel","error",
                            "-hide_banner",
                            "-user_agent",headers["User-Agent"],
                            "-analyzeduration","2147483647",
                            "-probesize","2147483647",
                            "-i",real_url,
                            '-bufsize','5000k',
                            "-map","0",
                            "-sn","-dn",
                            # "-f","mpegts",
                            # "-bsf:v","h264_mp4toannexb",
                            # "-c","copy",
                            #"-c:v","libx264",   #后期可以用crf来控制大小
                            "-c:v","copy",   #直接用copy的话体积特别大.
                            '-max_muxing_queue_size','64',
                            "{path}".format(path=file),
                        ], stderr = subprocess.STDOUT)                    

                    recordfinish=True
                    counttime=time.time()  
                    if startname in recording:                        
                        recording.remove(startname) 
                    print('\n'+startname+" "+ time.strftime('%Y-%m-%d %H:%M:%S  ') + '直播录制完成\n')
                    logger.warning(startname+" "+"直播录制完成")
                except subprocess.CalledProcessError as exc:
                    #logging.warning(str(exc.output))
                    print(str(exc.output))


            else:

                filename=startname + '_' + now + ".ts"
                if len(videopath)==0:
                    print("\r"+startname+" 录制视频中: "+os.getcwd()+"\\"+startname +'\\'+ filename)
                else:
                    print("\r"+startname+" 录制视频中: "+videopath+startname +'\\'+ filename)

                ffmpeg_path = "ffmpeg"         
                file = videopath+startname +'\\'+ filename
                try:
                    recording.append(startname)
                    _output = subprocess.check_output([
                        ffmpeg_path, "-y",
                        "-v","verbose", 
                        "-timeout","10000000", # 10s
                        "-loglevel","error",
                        "-hide_banner",
                        "-user_agent",headers["User-Agent"],
                        "-analyzeduration","2147483647",
                        "-probesize","2147483647",
                        "-i",real_url,
                        '-bufsize','5000k',
                        "-map","0",
                        "-sn","-dn",
                        "-f","mpegts",
                        # "-bsf:v","h264_mp4toannexb",
                        # "-c","copy",
                        "-c:v","copy",
                        '-max_muxing_queue_size','64',
                        "{path}".format(path=file),
                    ], stderr = subprocess.STDOUT)


                    recordfinish=True
                    counttime=time.time()
                    if startname in recording:                        
                        recording.remove(startname) 
                    print('\n'+startname+" "+ time.strftime('%Y-%m-%d %H:%M:%S  ') + '直播录制完成\n')
                    logger.warning(startname+" "+"直播录制完成")
                except subprocess.CalledProcessError as exc:
                    #logging.warning(str(exc.output))
                    print(str(exc.output))




        else:    
            #print('直播间不存在或未开播')
            pass




        if recordfinish==True:   
            counttimeend=time.time()-counttime
            if counttimeend<60:
                x=2
            else:
                recordfinish=False
        else:
            x=delaydefault

        while x:
            x = x-1
            #print('\r循环等待%d秒 '%x)
            if looptime:
                print('\r循环等待%d秒 '%x ,end="")
            time.sleep(1)
        if looptime:   
            print('\r检测直播间中...',end="") 





def displayinfo():
    time.sleep(10)
    while True:
        if len(recording)==0:
            time.sleep(10)
            nowdate=time.strftime("%H:%M:%S", time.localtime())
            print("\r没有正在录制的直播 "+nowdate,end="")
            print("")
            
            continue
        else:
            print("x"*30)
            NoRepeatrecording = list(set(recording))
            nowdate=time.strftime("%H:%M:%S", time.localtime())
            print("正在录制%i个直播: "%len(NoRepeatrecording)+nowdate)
            for x in NoRepeatrecording:
                print(x+" 正在录制中")
            print("%i个直播正在录制中: "%len(NoRepeatrecording)+nowdate)
            print("x"*30)
            time.sleep(10)
    



t = threading.Thread(target=displayinfo, args=(), daemon=True)
t.start()


runingList=[]
texturl=[]
textNoRepeatUrl=[]
createVar = locals()
zz=0
namelist=[]
while True:
    
    file=open("URL_config.ini","r",encoding="utf-8-sig")
    

    for line in file:
        
        line=line.strip()
        if line.startswith("#"):
            continue
        c=line.split()
        if len(c)==0:
            continue

        else:

            c=line.strip()

            c=c.split('#')
            if len(line)<20:
                continue
            
            texturl.append(line)

            

            #print(c[0])
    while len(namelist):    
        a=namelist.pop()
        replacewords = a.split('|')
        updateFile(r"URL_config.ini", replacewords[0], replacewords[1]) 
        #print(a)

    #格式化后查找不一样


    file.close()
    if len(texturl)>0:
        textNoRepeatUrl = list(set(texturl))

    # number=[1,2,3,4,5]
    # if 1 in number:
    #     print("1 in number")
    # if 0 not in number:
    #     print("0 not in number")


    if len(textNoRepeatUrl)>0:
        for i in textNoRepeatUrl:
            formatcontent = i.split(',')
            #formatcontent[0] #这个为分离出的地址
            if formatcontent[0] not in runingList:
                #print("新增链接: "+ formatcontent[0])
                zz=zz+1

                createVar['thread'+ str(zz)] = threading.Thread(target=startgo,args=(i,))
                createVar['thread'+ str(zz)].setDaemon(True)
                createVar['thread'+ str(zz)].start()
                runingList.append(formatcontent[0])
    texturl=[]
    
    #print("运行列表:"+ str(runingList))

    # newlyAdded=set(textNoRepeatUrl).difference(set(runingList))

    





    # if len(newlyAdded)>0:
    #     for x in newlyAdded:    
    #         runingList.append(x)
    #         print("新增链接: "+x)
    #         zz=zz+1
    #         createVar['thread'+ str(zz)] = threading.Thread(target=startgo,args=(line,))
    #         createVar['thread'+ str(zz)].setDaemon(True)
    #         createVar['thread'+ str(zz)].start()
    #     texturl=[]
    #     textNoRepeatUrl=[] #'清空列表'
    # else:
    #     print("运行列表:"+ str(runingList))


    time.sleep(3)





#print('程式结束,请按任意键退出')
input()   


