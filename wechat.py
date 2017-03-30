from flask import Flask, request, make_response, send_from_directory, abort
from random import randint
from lxml import etree
from imp import reload
from urllib.parse import quote, unquote
from collections import deque
from collections import defaultdict
import xml.etree.ElementTree as ET
import requests
import hashlib
import config
import reply
import receive
import random
import time
import chatter
import os
import threading

app = Flask(__name__)
token = '91930762d6cc738b'
joke_url = 'http://www.qiushibaike.com/hot/page/{page}/'
cache_content = defaultdict(deque)
handle_queue = deque()
sender_queue = deque()
lock = threading.Condition()

def get_keywords():
    reload(config)
    keywords = config.Config.keys()
    return '、'.join(keywords)

def get_content(content):
    reload(config)
    contentlist = deque()
    for x in config.Config:
        if x in content:
            module = __import__(config.Config[x][0]) # import module
            reload(module)
            c = getattr(module,config.Config[x][1])
            try:
                contentlist = cache_content[module]
                if len(contentlist) == 0:
                    contentlist = deque(c().getContent(content))
                    cache_content[module] = contentlist
                return contentlist.popleft()
            except Exception as e:
                print(str(e))
                raise e
            break
    else:
        contentlist = cache_content[content]
        if len(contentlist) == 0:
            reload(chatter)
            contentlist = deque([chatter.Chatter().getContent(content)])
            cache_content[content] = contentlist
        return contentlist.popleft()

    return {'type':'text', 'content':content}

class Handler(threading.Thread):
    def __init__(self, lock):
        self._lock = lock
        threading.Thread.__init__(self)
 
    def run(self):
        while True:
            if self._lock.acquire():
                tick()
                self._lock.release()
            time.sleep(0.05)

    def tick(self):
        if len(handle_queue) == 0:
            return

        recMsg = handle_queue.popleft()
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        replyMsg = reply.Msg(toUser, fromUser)
        if isinstance(recMsg, receive.TextMsg):
            content = recMsg.Content
            response = get_content(content)
            msgType = response['type']
            content = response['content']
            if msgType == 'text':
                replyMsg = reply.TextMsg(toUser, fromUser, content)
            elif msgType == 'news':
                replyMsg = reply.NewsMsg(toUser, fromUser, response['title'], response['content'], response['pic_url'], response['url'])
        elif isinstance(recMsg, receive.ImageMsg):
            pass
        elif isinstance(recMsg, receive.EventMsg):
            if recMsg.Event == 'subscribe':
                content = config.Welcome.format(key=get_keywords())
                replyMsg = reply.TextMsg(toUser, fromUser, content)

        sender_queue.append(replyMsg)

class Sender(threading.Thread):
    def __init__(self, lock):
        self._lock = lock
        threading.Thread.__init__(self)
 
    def run(self):
        while True:
            if self._lock.acquire():
                tick()
                self._lock.release()
            time.sleep(0.05)

    def tick(self):
        if len(sender_queue) == 0:
            return

        replyMsg = sender_queue.popleft()
        replyMsg.send()

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
    try:
        if request.method == 'GET':
            data = request.args
            print('Coming Get', data)
            if not data:
                return flask.render_template('index.htm')

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
            if (hashlib.sha1(s).hexdigest() != signature):
                return 'failed'
            
            return make_response(echostr)

        if request.method == 'POST':
            xml_str = request.stream.read()
            # print('Coming Post', xml_str)
            recMsg = receive.parse_xml(xml_str)
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            replyMsg = reply.Msg(toUser, fromUser)
            if isinstance(recMsg, receive.TextMsg):
                content = recMsg.Content
                response = get_content(content)
                msgType = response['type']
                content = response['content']
                if msgType == 'text':
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                elif msgType == 'news':
                    replyMsg = reply.NewsMsg(toUser, fromUser, response['title'], response['content'], response['pic_url'], response['url'])
            elif isinstance(recMsg, receive.ImageMsg):
                pass
            elif isinstance(recMsg, receive.EventMsg):
                if recMsg.Event == 'subscribe':
                    content = config.Welcome.format(key=get_keywords())
                    replyMsg = reply.TextMsg(toUser, fromUser, content)

            return replyMsg.send()
            
    except Exception as e:
        print(str(e))
        return ''

if __name__ == "__main__":
    # h = Handler(lock)
    # h.start()
    # s = Sender(lock)
    # s.start()
    app.run(host='0.0.0.0', port=80)