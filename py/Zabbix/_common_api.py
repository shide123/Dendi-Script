# -*- coding:utf-8 -*-
import json
import urllib2
import mysql
import time

# zabbix配置
global ZABBIX_URL, ZABBIX_USERNAME, ZABBIX_PASSWORD, HEADER, ACTION_NAME
ZABBIX_URL = 'http://172.16.251.116:8000/api_jsonrpc.php'
ZABBIX_USERNAME = "Admin"
ZABBIX_PASSWORD = "zabbix"
HEADER = {"Content-Type": "application/json"}
ACTION_NAME = "dingding"


# 监测服务器:
# zabbix mysql url:172.16.251.116:3306 user:root,password:123456，database：zabbix,table:hosts。
# 查询hostid方式：select hostid,host from zabbix.hosts where available=1;

# 通用请求
def _request(data):
    value = json.dumps(data).encode('utf-8')
    req = urllib2.Request(ZABBIX_URL, headers=HEADER, data=value)
    try:
        result = urllib2.urlopen(req)
        response = result.read()
        page = json.loads(response.decode('utf-8'))
        result.close()
        return page
    except Exception as e:
        print("Invaild request data ,please check again. the request data is :{}".format(data))
        return ""


# 获取授权token
def _get_auth():
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": ZABBIX_USERNAME,
            "password": ZABBIX_PASSWORD
        },
        "id": 1,
    }
    auth_ID = _request(data).get('result')
    return auth_ID


# 根据主机ip获取id
def _get_hostid(hostip):
    sql = "select hostid,host from hosts where status='0' and available='1'and host='%s'" % hostip
    results = mysql._query(sql)
    if len(results) > 1:
        return "null"
    else:
        return results[0][0]


# 获取相关数据
def _get_data(hostid, auth_ID, key):
    data = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": hostid,
            "search": {
                "key_": key
            },
            "sortfield": "name"
        },
        "auth": auth_ID,
        "id": 1
    }
    result = _request(data).get('result')
    return result


# 获取图形列表数据id
def _get_graph_list(hostid, auth_ID):
    data = {
        "jsonrpc": "2.0",
        "method": "graph.get",
        "params": {
            "output": "extend",
            "hostids": hostid,
            "sortfield": "name"
        },
        "auth": auth_ID,
        "id": 1
    }
    result = json.dumps(_request(data))
    print type(result)
    return result


def _get_graph(auth_ID):
    data = {
        "jsonrpc": "2.0",
        "method": "graphitem.get",
        "params": {
            "output": "extend",
            "graphids": "827"
        },
        "auth": auth_ID,
        "id": 1
    }
    result = json.dumps(_request(data))
    return result

# 获取actionid (action为钉钉)
def _get_action(ACTION_NAME):
    sql = "select actionid from actions where name = '%s'" % ACTION_NAME
    results = mysql._query(sql)
    if len(results) > 1:
        return "null"
    else:
        return results[0][0]


# 获取alert列表
def _get_alert(action_ID, auth_ID):
    time_pre15 = time.time() - 7 * 60 * 60 * 24
    data = {
        "jsonrpc": "2.0",
        "method": "alert.get",
        "params": {
            "output": "extend",
            "actionids": action_ID,
            "time_from": time_pre15
        },
        "auth": auth_ID,
        "id": 1
    }
    alert = json.dumps(_request(data))
    return alert


# 时间戳转换
def time():
    return 0

def _graph_image():

    #http://172.16.251.116:8000/chart2.php?graphid=827&period=60&stime=20180306170210&isNow=0&profileIdx=web.graphs&profileIdx2=827&width=1170&sid=41930b6a93f2a5f0&screenid=&curtime=1520328413800
    #refer to http://www.roncoo.com/article/detail/125469
    return 0


#获取主机列表（bj/office）中关键指标（cpu/network/memory/filesystem...）特殊处理(max/min/avg)
def _get_spec_items(time_interval,items,):

    return 0

if __name__ == '__main__':
    key = 'system'
    auth_ID = _get_auth()
    hostid = _get_hostid("123.456.789.11")
    # result = _get_data(hostid, auth_ID, key)
    graph = _get_graph_list(hostid, auth_ID)
    action_ID = _get_action(ACTION_NAME)
    alerts = _get_alert(action_ID, auth_ID)
    graph_test=_get_graph(auth_ID)
    print graph_test
