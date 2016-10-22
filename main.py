import requests
import time
from HTMLParser import *

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tim = "none"
        self.dis = "none"
        self.temp = ""
        self.type = "none"
        self.pted = 0
        self.strong = 0
        self.span = 0
    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None
        '''for attr in attrs:
            if attr[0] == "class":
                print attr[1]'''
        if tag == "strong":
            self.strong = 1
        if tag == "div" and _attr(attrs,"class") == "activity-type-date":
            '''print _attr(attrs,"class")
            print self.getpos()'''
            self.div = 1
    
    def handle_endtag(self, tag):
        if tag == "strong":
            self.strong = 0
        if tag == "div" :
            self.div = 0

    def handle_data(self, data):
        if self.strong == 1 and self.div == 1:
            print 6666
            self.type = data
        if data == "km":
            if ord(self.temp[0]) < 33:
                self.dis = float(self.temp[1:len(self.temp)])
            else:
                self.dis = float(self.temp)
        if data == "mi":
            if ord(self.temp[0]) < 33:
                self.dis = float(self.temp[1:len(self.temp)]) * 1.61
            else:
                self.dis = float(self.temp) * 1.61
        elif data == 'Moving Time':
            self.tim = self.temp
        if self.strong == 1:
            self.temp = data


headers ={
    "Referer": "https://www.strava.com/onboarding",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)AplleWebKit/601.6.17(KHTML,like Gecko) Version/9.1.1 Safari/601.6.17",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cache-Control":"maxp-age=0" }

f = open("data2","w")

r = requests.session()
rsp = r.post("https://www.strava.com/login",{"email": "1137201918@qq.com", "password": "zyl961127"},headers=headers)


# instantiate the parser and fed it some HTML
parser = MyHTMLParser()


for i in range(0,10):
    print i
    temp = "https://www.strava.com/activities/" + str(i + 746625478)
    html = r.get(temp)
    parser.dis = parser.tim = "-1"
    parser.feed(html.text)
    print parser.dis
    print parser.tim
    print parser.type
    if parser.dis != "-1" and parser.dis != "" and parser.dis != "s" and parser.tim != "-1" and parser.tim != "" and parser.tim != "s":
        f.write(str(i))
        f.write(',')
        f.write(str(parser.dis))
        f.write(',')
        f.write(parser.tim)
        f.write(',')
        f.write(parser.type)
        f.write('\n')
