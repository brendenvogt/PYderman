import requests

import urllib.request
from urllib.parse import urljoin
from urllib.parse import urlsplit, urlunsplit


from bs4 import BeautifulSoup
from datetime import datetime
import os
import uuid
import shutil


class PyterParker():

    def __init__(self, name, req="urllib", crawlDepth=0):
        self.name = name or self._getDateTime()
        self.url = url
        self.crawlDepth = crawlDepth
        self.req = req

        self.imgUrls = []
        self.subUrls = []

        self._imgDir = "img"
        self._graphDir = "graph"

    def run(self, url):
        html = self.grab(url)
        self.parse(url, html)

    def grab(self, url):
        html = ""
        if self.req == "urllib":
            html = urllib.request.urlopen(self.url).read()
        if self.req == "requests":
            html = requests.get(self.url).content
        return html

    def parse(self, url, content):
        # soup parsing
        soup = BeautifulSoup(content, 'html.parser')
        
        # url parsing
        urls = self.parseUrls(self._getBase(url), soup)
        self._printAll(urls)
        
        # imgs 
        imgs = self.parseImgs(soup)
        self._printAll(imgs)

    # Parse Methods

    def parseImgs(self, soup):
        imgs = soup.find_all("img")
        return [img.get("src") or img.get("data-lazyload") for img in imgs]
        
    def parseUrls(self, urlbase, soup):
        links = soup.find_all("a")
        cleaned = []
        for link in links:
            link = link.get("href")
            if link and self._isRelative(link):
                link = urljoin(url, link[1:])
            if link and link != "":
                cleaned.append(link)
        return cleaned

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

    def _getBase(self, url):
        split_url = urlsplit(url)
        clean_path = "".join(split_url.path.rpartition("/")[:-1])
        clean_url = urlunsplit((split_url.scheme, split_url.netloc, "", "", ""))
        return clean_url

    def _isRelative(self, url):
        return url[0] == "#" or url[0] == "/"

    def _getDateTime(self):
        return datetime.utcnow().strftime("%d-%m-%y-%H-%M-%S")

    def _printAll(self, items):
        for i in items:
            print(i)

    def _isValid(self, url):
        try:
            if self.req == "urllib":
                r = urllib.request.urlopen(url)
                return r.getcode() == 200
            if self.req == "requests":
                r = requests.get(url)
                return r.status_code == 200
            return False
        except:
            return False

if __name__ == "__main__":
    print("My spider senses are tingling")

    # url = "https://www.amazon.com/TCL-49S405-49-Inch-Ultra-Smart/dp/B01MYGISTO/ref=sr_1_1_sspa?s=tv&ie=UTF8&qid=1536346649&sr=1-1-spons&keywords=tv&psc=1"
    url = "https://www.iherb.com/pr/p/11242"
    parser = PyterParker(name=None, req="requests", crawlDepth=2)
    parser.run(url)

    # ##IMAGES
    # parser.saveImages()	
    # ##GRAPH
    # parser.saveGraph()
