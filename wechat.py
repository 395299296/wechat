from flask import Flask, request, make_response, send_from_directory, abort
from random import randint
from lxml import etree
from imp import reload
from urllib.parse import quote, unquote
import xml.etree.ElementTree as ET
import requests
import hashlib
import config
import random
import time
import chatter
import os

app = Flask(__name__)
token = '91930762d6cc738b'
joke_url = 'http://www.qiushibaike.com/hot/page/{page}/'
cache_content = {}

def get_keywords():
    reload(config)
    keywords = config.Config.keys()
    return '、'.join(keywords)

def get_content(content):
    reload(config)
    contentlist = []
    for x in config.Config:
        if x in content:
            module = __import__(config.Config[x][0]) # import module
            reload(module)
            c = getattr(module,config.Config[x][1])
            try:
                if module in cache_content and cache_content[module]['time'] >= time.time() - 15:
                    contentlist = cache_content[module]['list']
                else:
                    contentlist = c().getContent(content)
                    cache_content[module] = {'time':time.time(),'list':contentlist}
            except Exception as e:
                print(str(e))
                raise e
            break
    else:
        if content in cache_content and cache_content[content]['time'] >= time.time() - 15:
            contentlist = cache_content[content]['list']
        else:
            reload(chatter)
            response = chatter.Chatter().getContent(content)
            cache_content[content] = {'time':time.time(),'data':response}
            contentlist = response

    if len(contentlist) > 0:
        return contentlist[randint(0, len(contentlist)-1)]

    return {'type':'text', 'content':content}

@app.route('/girl/<filename>',methods=['GET'])
def download(filename):
    filename = unquote(filename)
    print(filename)
    if request.method == "GET":
        if os.path.isfile(os.path.join('girl', filename)):
            return send_from_directory('girl', filename)
        abort(404)

@app.route('/',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        data = request.args
        print('Coming Get', data)
        test = data.get('test','')
        if test != '':
            content = get_content(test)
            return content['content']
        
        signature = data.get('signature','')
        if signature == '':
            return 'error'

        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s).encode('utf8')
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)

    if request.method == 'POST':
        xml_str = request.stream.read()
        xml = ET.fromstring(xml_str)
        toUserName=xml.find('ToUserName').text
        fromUserName = xml.find('FromUserName').text
        createTime = xml.find('CreateTime').text
        msgType = xml.find('MsgType').text
        if msgType != 'text':
            if msgType == 'event':
                msgType = 'text'
                event = xml.find('Event').text
                if event == 'subscribe':
                    content = config.Welcome.format(key=get_keywords())
                else:
                    content = 'success'
            else:
                content = '格式错误'
        else:
            content = xml.find('Content').text
            print(content)
            msgId = xml.find('MsgId').text
            response = get_content(content)
            msgType = response['type']
            content = response['content']

        if msgType == 'text':
            reply = '''
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[%s]]></Content>
                    </xml>
                    ''' % (fromUserName, toUserName, createTime, content)
        elif msgType == 'news':
            reply = '''
                    <xml>
                    <ToUserName><![CDATA[%s]]></ToUserName>
                    <FromUserName><![CDATA[%s]]></FromUserName>
                    <CreateTime>%s</CreateTime>
                    <MsgType><![CDATA[news]]></MsgType>
                    <ArticleCount>1</ArticleCount>
                    <Articles>
                        <item>
                            <Title><![CDATA[%s]]></Title> 
                            <Description><![CDATA[%s]]></Description>
                            <PicUrl><![CDATA[%s]]></PicUrl>
                            <Url><![CDATA[%s]]></Url>
                        </item>
                    </Articles>
                    </xml>
                    ''' % (fromUserName, toUserName, createTime, response['title'], response['content'], response['pic_url'], response['url'])
        return reply

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8020)