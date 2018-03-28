# -*- coding: utf-8 -*-
import cookielib, urllib2, urllib

class Zabbix_api():

    def __init__(self, url="http://172.16.251.116:8000/index.php", name="Admin", password="zabbix"):

        self.url = url

        self.name = name

        self.passwd = password

        # 初始化的时候生成cookies

        cookiejar = cookielib.CookieJar()

        urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

        values = {"name": self.name, 'password': self.passwd, 'autologin': 1, "enter": 'Sign in'}

        data = urllib.urlencode(values)

        request = urllib2.Request(url, data)

        try:

            urlOpener.open(request, timeout=10)

            self.urlOpener = urlOpener

        except urllib2.HTTPError, e:

            print e

    def GetGraph(self, url="http://172.16.251.116:8000/chart2.php",
                 values={'width': 800, 'height': 200, 'graphid': '827', 'period': 604800}, image_dir="/tmp"):
        data = urllib.urlencode(values)
        request = urllib2.Request(url, data)
        url = self.urlOpener.open(request)
        image = url.read()
        imagename = "%s/%s.jpg" % (image_dir, values["graphid"])
        f = open(imagename, 'wb')
        f.write(image)
        return '1'


if __name__ == "__main__":
    graph = Zabbix_api()

    values = {'width': 800, 'height': 200, 'graphid': '827', 'period': 3600}

    graph.GetGraph("http://172.16.251.116:8000/chart2.php", values, "/tmp")
