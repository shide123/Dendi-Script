# -*- coding:utf-8 -*-
import datetime
import main
from elasticsearch import Elasticsearch

class ElasticSearchUtil:
    def __init__(self, host):
        self.host = host
        self.conn = Elasticsearch([self.host])

    def __del__(self):
        self.close()

    def check(self):
        '''
        输出当前系统的ES信息
        :return:
        '''
        return self.conn.info()

    def searchDoc(self, index=None, type=None, body=None):
        '''
        查找index下所有符合条件的数据
        :param index:
        :param type:
        :param body: 筛选语句,符合DSL语法格式
        :return:
        '''
        return self.conn.search(index=index, doc_type=type, body=body)

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception, e:
                pass
            finally:
                self.conn = None


def mysql_monitor():
    print "------start monitor mysql-----"
    host = '172.16.251.116:9200'
    esAction = ElasticSearchUtil(host)
    nowtime = datetime.datetime.now().strftime("%Y.%m.%d")
    indices = "mysql-%s" % nowtime
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"_index": "%s"}}
                ],
                "filter": [
                    {"range": {"@timestamp": {"gte": "now-15m", "lte": "now"}}}
                ],
                "must_not": [
                    {
                        "match": {
                            "clientip": "(123.345.456.11) AND (123.345.456.11))"
                        }
                    }
                ]
            }
        }
    }
    mysql_index = {"_index": indices}
    whitelist = "(123.345.456.11) AND (123.345.456.11)) AND(123.345.456.11) AND (123.345.456.11)"
    whitelist_dic = {"clientip": whitelist}
    query["query"]["bool"]["must"].__getitem__(0).get("match").update(mysql_index)
    query["query"]["bool"]["must_not"].__getitem__(0).get("match").update(whitelist_dic)
    total = (esAction.searchDoc(indices, None, query))["hits"]["total"]
    if total != 0:
        latest_record = (esAction.searchDoc(indices, None, query))["hits"]["hits"][0]["_source"]["message"]
        message = "found %s records, unknow server connected to mysql server, the latest message is : %s" % (
            total, latest_record)
        main.send_text_to_chat(message)
    # mysql query_time gte 0.5 s
    query_time = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "clientip": "(123.345.456.11) AND (123.345.456.11))"
                    }
                },
                "must_not": {
                    "range": {
                        "query_time": {
                            "lte": 0.5
                        }
                    }
                },
                "filter": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-15m",
                                "lte": "now"
                            }
                        }
                    }
                ],
                "should": [
                    {
                        "match": {
                            "_index": "mysql-2018.01.29"
                        }
                    }
                ]
            }
        }

    }
    print query_time["query"]["bool"]["should"][0].get("match")
    query_time["query"]["bool"]["should"][0].get("match").update(mysql_index)
    whitelist = "(123.345.456.11) AND (123.345.456.11))"
    whitelist_dic = {"clientip": whitelist}
    query_time["query"]["bool"]["must"].get("match").update(whitelist_dic)
    total_time = (esAction.searchDoc(indices, None, query_time))["hits"]["total"]
    print esAction.searchDoc(indices, None, query_time)
    print total_time
    if total_time != 0:
        query_latest_record = (esAction.searchDoc(indices, None, query_time))["hits"]["hits"][0]["_source"]["message"]
        message = "%s mysql query_time gte 0.5s. the latest messages: %s " % (total_time, query_latest_record)
        print message
        main.send_text_to_chat(message)


def cpp_monitor():
    return 0


def nginx_monitor():
    print "------start monitor nginx -----"
    host = '172.16.251.116:9200'
    esAction = ElasticSearchUtil(host)
    nowtime = datetime.datetime.now().strftime("%Y.%m.%d")
    indices = "nginx-%s" % nowtime
    nginx_index = {"_index": indices}
    # monitor responsetime avg gte 0.5s latest 15min
    query_response = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "_index": "nginx-2018.02.04"
                    }
                },
                "filter": [
                    {
                        "range": {
                            "@timestamp": {
                                "gte": "now-15m",
                                "lte": "now"
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "avg_response": {
                "avg": {
                    "field": "responsetime"
                }
            }
        }
    }
    query_response["query"]["bool"]["must"].get("match").update(nginx_index)
    print query_response["query"]["bool"]["must"].get("match")
    avg_response = esAction.searchDoc(indices, None, query_response)["aggregations"]["avg_response"]["value"]
    print avg_response
    if avg_response >= 1:
        message = "nginx avg response time gte 1.0s latest 15min ,avg responsetime %s" % avg_response
        main.send_text_to_chat(message)
    return 0

if __name__ == '__main__':
    nginx_monitor()
