import requests
from bs4 import BeautifulSoup
import re
import _thread
import os, sys
import configparser
import urllib
import smtp3

conf = configparser.ConfigParser()
conf.read(os.getcwd() + '\\conf.ini')
sections = conf.sections()


def get_web(url):
    header = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Connection':
        'keep-alive',
        'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    wbdata = requests.get(url, headers=header).content
    soup = BeautifulSoup(wbdata, 'lxml')

    element = ''
    datas=[]
    for section in sections:
        items = conf.items(section)
        for item in items:
            if item[0] == 'element':
                elem = item[1] 
                elements = soup.select(elem)

                
                i=0
                while i<len(elements):
                    Type=elements[i].text                    
                    Title=elements[i+1].text
                    Content=elements[i+1].contents
                    Area=elements[i+2].text
                    Time=elements[i+3].text
                    i+=4;

                    data = {
                        'type': Type, 
                        'title': Title, 
                        'content':Content,
                        'area': Area, 
                        'time': Time
                        }
                    print(data)
                    datas.append(data)
    print(datas)

    content='<table><tbody><th>类型</th><th>标题</th><th>地区</th><th>发布时间</th>'
    for data in datas:
        content +='<tr>'
        content+='<td>'+str(data['type'])+'</td>'
        s = str(data['content'][1].attrs['onclick']).replace('\\n','').replace('','')
        content+='<td><a href="'+s[s.index("http"):s.index("html")]+'html">'+data['content'][1].text+ '</a></td>'
        content+='<td>'+str(data['area'])+'</td>'
        content+='<td>'+str(data['time'])+'</td>'
        content+='</tr>'
    content+='</tbody></table>'

    try:
        smtp3.send_email('近期招标通知-招标采集平台自动发送',content)
    except Exception as e:
        print('邮件发送失败:'+e.args[0]) 

if __name__ == '__main__':
    for section in sections:
        items = conf.items(section)
        url = items[0][1]
        del items[0]
        for item in items:
            if -1 == item[0].find('element'):
                val = urllib.parse.quote_plus(item[1], encoding='gbk')
                url += '&' + item[0] + '=' + val
            #else:
            # url+='&' + item[0] + '=' +item[1]
        print(url)
        try:
            _thread.start_new_thread(get_web(url))
        except Exception as e:
            print('-------------' + e.args[0] + '-------------------------')
