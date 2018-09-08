import requests
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import os
import uuid
import shutil



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
        html = self.grab(self.url)
        self.parse(url, html)

    def grab(self, url):
        html = ""
        if self.req == "urllib":
            html = urllib.request.urlopen(self.url).read()
        if self.req == "requests":
            html = requests.get(self.url).content
        return html

    def parse(self, url, content):
        soup = BeautifulSoup(content, 'html.parser')
        self.parseImgs(url, soup)
        self.parseUrls(url, soup)

    # Parse Methods

    def parseImgs(self, url, soup):
        imgs = soup.find_all("img")
        for img in imgs:
            imgUrl = img.get("src") or img.get("data-lazyload")
            self.imgUrls.append((url, imgUrl))

    def parseUrls(self, url, soup):
        links = soup.find_all("a")
        for link in links:
            linkUrl = link.get("href")
            self.subUrls.append((url, linkUrl))

    # Save Methods

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

    # Helper

    def _getDateTime(self):
        return datetime.utcnow().strftime("%d-%m-%y-%H-%M-%S")


if __name__ == "__main__":
    print("My spider senses are tingling")

    # url = "https://www.amazon.com/TCL-49S405-49-Inch-Ultra-Smart/dp/B01MYGISTO/ref=sr_1_1_sspa?s=tv&ie=UTF8&qid=1536346649&sr=1-1-spons&keywords=tv&psc=1"
    url = "https://www.iherb.com/pr/p/11242"
    parser = PyterParker(url=url, name=None, req="requests", crawlDepth=2)
    parser.run()

    ##IMAGES
    parser.saveImages()	
    ##GRAPH
    parser.saveGraph()
