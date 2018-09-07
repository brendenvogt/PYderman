from bs4 import BeautifulSoup
import os
import shutil

import requests
import urllib.request

import uuid
from datetime import datetime

class PyterParker():

    def __init__(self, url, name, req="urllib", crawlDepth=0):
        self.name = name or self._getDateTime()
        self.url = url
        self.crawlDepth = crawlDepth
        self.req = req

        self.imgUrls = []
        self.subUrls = []

        self._imgDir = "img"
        self._graphDir = "graph"

    def run(self):
        self.grab(self.url, 0)

    def grab(self, url, depth):
        #get html content
        html = ""
        if self.req == "urllib":
            html = urllib.request.urlopen(self.url).read()
        if self.req == "requests":
            html = requests.get(self.url).content
        #parse html
        self.parse(url, html)

    def parse(self, source, content):
        #parse html
        soup = BeautifulSoup(content, 'html.parser')
        self.parseImgs(source, soup)
        self.parseSubUrls(source, soup)
        # print(soup.prettify())

    def parseImgs(self, source, soup):
        imgs = soup.find_all("img")
        for i in imgs:
            x = i.get("src") or i.get("data-lazyload")
            self.imgUrls.append((source, x))

    def parseSubUrls(self, source, soup):
        imgs = soup.find_all("a")
        for i in imgs:
            x = i.get("href")
            self.subUrls.append((source, x))

    #todo def createGraph(): # create tree diagram

    def saveImages(self):
        base = self.name+"/"+self._imgDir
        if not os.path.exists(base):
            os.makedirs(base)
        for imgTup in self.imgUrls:	
            img = imgTup[1]
            response = requests.get(img, stream=True)
            with open(base+"/"+str(uuid.uuid4())+"_"+img[img.rfind("/")+1:], 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

    def saveGraph(self):
        import csv
        base = self.name+"/"+self._graphDir
        if not os.path.exists(base):
            os.makedirs(base)
        with open(base+"/"+'graph.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            for i in self.subUrls:
                writer.writerow(i)

    def _getDateTime(self):
        return datetime.utcnow().strftime("%d-%m-%y-%H-%M-%S")

if __name__ == "__main__":
    print("hello")

    url = "https://www.amazon.com/TCL-49S405-49-Inch-Ultra-Smart/dp/B01MYGISTO/ref=sr_1_1_sspa?s=tv&ie=UTF8&qid=1536346649&sr=1-1-spons&keywords=tv&psc=1"
    parser = PyterParker(url=url, name=None, req="urllib")
    parser.run()

    ###SAVE DIFFERENT TYPES OF OBJECTS

    ##IMAGES
    parser.saveImages()	
    ##GRAPH
    parser.saveGraph()
