import requests
import time
from HTMLParser import *

'''use class MyHTMLParser() to orientate data that are needed in each page, more specific explanation about this class can be found in "https://docs.python.org/2/library/htmlparser.html" '''
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
        if tag == "strong":
            self.strong = 1
        if tag == "div" and _attr(attrs,"class") == "activity-type-date":
            self.div = 1
    
    def handle_endtag(self, tag):
        if tag == "strong":
            self.strong = 0
        if tag == "div" :
            self.div = 0

    def handle_data(self, data):
        '''scrape the tyoe data (Run, Ride etc.)'''
        if self.strong == 1 and self.div == 1:
            self.type = data
        '''scrape the distance data (using the fact that the next data is string "km" in the webpage)'''
        if data == "km":
            if ord(self.temp[0]) < 33:
                self.dis = float(self.temp[1:len(self.temp)])
            else:
                self.dis = float(self.temp)
        '''scrape the distance data that is in "mile" unit'''
        if data == "mi":
            if ord(self.temp[0]) < 33:
                self.dis = float(self.temp[1:len(self.temp)]) * 1.61
            else:
                self.dis = float(self.temp) * 1.61
        elif data == 'Moving Time':
            '''scrape the time data (using fact that the next data is string "Moving Time" in the webpage)'''
            self.tim = self.temp
        if self.strong == 1:
            self.temp = data


headers ={
    "Referer": "https://www.strava.com/onboarding",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)AplleWebKit/601.6.17(KHTML,like Gecko) Version/9.1.1 Safari/601.6.17",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cache-Control":"maxp-age=0" }

f = open("strava_data_8","w")

r = requests.session()
rsp = r.post("https://www.strava.com/login",{"email": "1137201918@qq.com", "password": "zyl961127"},headers=headers)


# instantiate the parser and fed it some HTML
parser = MyHTMLParser()

'''in the following loop, I can change the page of activity and scrape each page's data. Meanwhile  "print i " can show how many page has been seen '''
for i in range(0,3000):
    print i
    temp = "https://www.strava.com/activities/" + str(i + 746648001)
    html = r.get(temp)
    parser.dis = parser.tim = "-1"
    parser.feed(html.text)
    '''This determine statment mainly judges whether the data is NA or not, if it is NA then it will not be written in the data collection text'''
    if parser.dis != "-1" and parser.dis != "" and parser.dis != "s" and parser.tim != "-1" and parser.tim != "" and parser.tim != "s":
        f.write(str(i + 746648001))
        f.write(',')
        f.write(str(parser.dis))
        f.write(',')
        f.write(parser.tim)
        f.write(',')
        f.write(parser.type)
        f.write('\n')
