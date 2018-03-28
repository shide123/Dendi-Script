# -*- coding:utf-8 -*-
import urllib2
import json
import monitor


def _send_msg(url, token, body):
    posturl = url + token
    headers = {'Content-Type': 'application/json'}
    request = urllib2.Request(url=posturl, headers=headers, data=body)
    response = urllib2.urlopen(request)
    resp = response.read()
    print(resp)


def send_text_to_chat(text):
    access_token= "7db148bb9091c6cf4659eac5174a5721427aa523e7d9864eab660771389c28c4"
    msg_type, msg = _gen_text_msg(text)
    return _send_msg_to_chat(access_token, msg_type, msg)

def _send_msg_to_chat(access_token, msg_type, msg):
    body_dict = {
        "msgtype": msg_type
    }
    body_dict[msg_type] = msg
    body = json.dumps(body_dict)
    return _send_msg("https://oapi.dingtalk.com/robot/send?access_token=", access_token, body)


def _gen_text_msg(text):
    msg_type = 'text'
    msg = {"content": text}
    return msg_type, msg


if __name__ == '__main__':
    # body = monitor.check()
    # if body != None:
    send_text_to_chat( )
