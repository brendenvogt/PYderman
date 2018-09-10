import requests

import urllib.request
from urllib.parse import urljoin
from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup
from datetime import datetime
import os
import uuid
import shutil
import csv

from slugify import slugify
from tqdm import tqdm 

class Scrape():

    def __init__(self, source="", urls=[], htmls=[], txts=[], pdfs=[], csvs=[], xmls=[], imgs=[], mp3s=[], mp4s=[]):
        self.source = source
        self.urls = urls
        # standard
        self.htmls = htmls
        self.txts = txts
        self.pdfs = pdfs
        # data
        self.csvs = csvs
        self.xmls = xmls
        # media
        self.imgs = imgs
        self.mp3s = mp3s
        self.mp4s = mp4s

    def report(self):
        print(f"Scrape Report from: {self.source}")
        print(f"- number of urls: {len(self.urls)}")
        print(f"- number of html urls: {len(self.htmls)}")
        print(f"- number of txt urls: {len(self.txts)}")
        print(f"- number of txt urls: {len(self.pdfs)}")
        print(f"- number of csv urls: {len(self.csvs)}")
        print(f"- number of xml urls: {len(self.xmls)}")
        print(f"- number of img urls: {len(self.imgs)}")
        print(f"- number of mp3 urls: {len(self.mp3s)}")
        print(f"- number of mp4 urls: {len(self.mp4s)}")

class Pyderman():

    def __init__(self, name=None, url="", req="requests", depth=0, stayInternal=False):
        self.name = name or self._getDateTime()
        self.url = url
        self.depth = depth
        self.req = req
        self.stayInternal = stayInternal

        self.seen = set()
        self.scrapes = []

        self._imgDir = "img"
        self._graphDir = "graph"
        self._csvDir = "csv"

    def run(self):
        self.crawl(self.url, self.depth)

    def crawl(self, url, depth):
        if url in self.seen:
            return
        self.seen.add(url)

        scrape = self.scrape(url)
        self.scrapes.append(scrape)
        
        if (depth != 0):
            toSearch = self._filter(scrape.urls, self.seen)
            for i in toSearch:
                self.crawl(i, depth-1)

    def scrape(self, url):
        html = self.grab(url)
        soup = BeautifulSoup(html, 'html.parser')

        scrape = Scrape(source=url)

        urlBase = self._getBase(url)

        # url parsing
        scrape.urls = self.parseUrls(urlBase, soup)
        # self._printAll(scrape.urls)

        # # imgs 
        scrape.imgs = self.parseImgs(urlBase, soup)
        # # self._printAll(scrape.imgs)

        # csvs 
        scrape.csvs = self.parseCsvs(urlBase, soup)
        # self._printAll(scrape.csvs)

        return scrape


    def grab(self, url):
        html = ""
        if url == None or url == "":
            return html
        try:
            if self.req == "urllib":
                html = urllib.request.urlopen(url).read()
            if self.req == "requests":
                html = requests.get(url).content
            return html
        except:
            return html

    # Parse Methods

    def parseImgs(self, urlbase, soup):
        urls = soup.find_all("img")
        urls = [url.get("src") or url.get("data-lazyload") for url in urls]
        urls = self.clean(urls, urlbase)
        return urls

    def parseUrls(self, urlbase, soup):
        urls = soup.find_all("a")
        urls = [url.get("href") for url in urls]
        urls = self.clean(urls, urlbase)
        return urls
        
    def parseTxts(self, urlbase, soup):
        pass        

    def parseXmls(self, urlbase, soup):
        pass

    def parseCsvs(self, urlbase, soup):
        urls = soup.find_all("a")
        urls = [url.get("href") for url in urls]
        urls = [url if self._isType(url, ".csv") else None for url in urls]
        urls = self.clean(urls, urlbase)
        return urls
        
    def parsePdfs(self,urlbase, soup):
        pass

    def clean(self, urls, urlbase):
        cleaned = set()
        for url in urls:
            if url:
                
                if self._isRelative(url):
                    url = urljoin(urlbase, url)
                
                if len(url) > 2 and url[:2] == "//":
                    url = "http:"+url
                
                if url != "":
                    if self.stayInternal == True:
                        if self._getDomain(url) != self._getDomain(urlbase):
                            continue
                    cleaned.add(url)

        return list(cleaned)

    # Save Methods

    def saveImages(self):
        print("Saving All Images")
        for scrape in tqdm(self.scrapes):
            print(f"Saving images from: {scrape.source}")
            self.saveImagesForScrape(scrape)

    def saveImagesForScrape(self, scrape):
        base = self._slugify(scrape.source)
        source = self._slugify(self.url)
        base = source+"/"+self._imgDir+"/"+base
        if not os.path.exists(base):
            os.makedirs(base)
        
        for img in scrape.imgs:	
            try:
                response = requests.get(img, stream=True)
                with open(base+"/"+str(uuid.uuid4())+"_"+img[img.rfind("/")+1:], 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
            except Exception as e:
                print(f"error downloading: {img} with error {e}")

    def saveGraph(self):
        print("Saving All Graphs")
        for scrape in tqdm(self.scrapes):
            print(f"Saving graph from: {scrape.source}")
            self.saveGraphForScrape(scrape)

    def saveGraphForScrape(self, scrape):
        slug = self._slugify(scrape.source)
        source = self._slugify(self.url)
        base = source+"/"+self._graphDir+"/"+slug
        if not os.path.exists(base):
            os.makedirs(base)

        with open(base+"/"+'graph.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            for url in scrape.urls:
                writer.writerow([slug,scrape.source,url])

    def saveCsv(self):
        print("Saving All Csvs")
        for scrape in tqdm(self.scrapes):
            print(f"Saving csv from: {scrape.source}")
            self.saveCsvForScrape(scrape)

    def saveCsvForScrape(self, scrape):
        slug = self._slugify(scrape.source)
        source = self._slugify(self.url)
        base = source+"/"+self._csvDir+"/"+slug
        if not os.path.exists(base):
            os.makedirs(base)

        for file in scrape.csvs: 
            csvSlug = self._slugify(file)    
            try:
                response = requests.get(file, stream=True)
                with open(base+"/"+csvSlug+".csv", 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
            except Exception as e:
                print(f"error downloading: {file} with error {e}")

    # Helper
    
    def _slugify(self, string):
        return slugify(string)

    def _filter(self, source, destination):
        result = []
        for i in source:
            if i not in destination:
                result.append(i)
        return result

    def _getDomain(self, url):
        split_url = urlsplit(url)
        return split_url.netloc

    def _getBase(self, url):
        split_url = urlsplit(url)
        clean_url = urlunsplit((split_url.scheme, split_url.netloc, "", "", ""))
        return clean_url

    def _isRelative(self, url):
        return self._getBase(url) == ""

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

    def _getExtension(self, url):
        foundExt = os.path.splitext(url)
        return foundExt[1]

    def _isType(self, url, ext):
        foundExt = os.path.splitext(url)
        return foundExt[1] == ext

    def _hasExtension(self, url):
        foundExt = os.path.splitext(url)
        return foundExt[1] != ""

if __name__ == "__main__":
    print("My spidey senses are tingling")

    # url = "https://www.google.com/"
    url = "https://support.spatialkey.com/spatialkey-sample-csv-data/"

    parser = Pyderman(url=url, depth=0)
    parser.run()

    ##IMAGES
    # parser.saveImages()	

    ##GRAPH
    # parser.saveGraph()

    ##CSV
    # parser.saveCsv()

    ##Print Out Report 
    for scrape in parser.scrapes:
        scrape.report()

    # TODO
    # 1. Be able to limit crawling to internal links vs internal and external links
    # 2. Be able to scrape for files such as txt, csv, and xml

