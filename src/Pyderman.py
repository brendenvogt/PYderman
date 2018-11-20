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

import re

import json
import xml.etree.ElementTree as ET

from Scrape import Scrape


class Pyderman():

    def __init__(self, name=None, url="", req="requests", depth=0, stayInternal=False):
        self.name = name or self._getDateTime()
        self.url = url
        self.depth = depth
        self.req = req
        self.stayInternal = stayInternal

        self.seen = set()
        self.scrapes = []

        self._graphDir = "graph"
        #
        self._imgDir = "img"
        self._mp3Dir = "mp3"
        self._mp4Dir = "mp4"
        #
        self._htmlDir = "html"
        self._txtDir = "txt"
        self._pdfDir = "pdf"
        #
        self._csvDir = "csv"
        self._xmlDir = "xml"

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
        content = self.grab(url)
        if self._isJson(content):
            return self.scrapeJson(content, url)
        elif self._isXml(content) or self._isHtml(content):
            return self.scrapeHtXml(content, url)

    def scrapeJson(self, content, url):

        urls = self._getUrls(str(content))

        # soup = json.loads(content)
        # urls = self.grabJsonUrls(soup)

        scrape = Scrape(source=url)

        scrape.urls = urls

        urlBase = self._getBase(url)

        return scrape

    def grabJsonUrls(self, items):
        result = []
        if (type(items) == list):
            for i in items:
                return self.grabJsonUrls(i) + result
        elif (type(items) == dict):
            for key, value in items.items():
                if (type(value) == dict or type(value) == list):
                    result = result + self.grabJsonUrls(value)
                elif (type(value) != str):
                    continue
                else:
                    if (self._isAbsoluteUrl(value)):
                        result.append(value)
                    # elif (self._isRelativeUrl(value)):
                    #     absolute = self._makeAbsolute(self.url, value)
                    #     result.append(absolute)
        return result

    def scrapeHtXml(self, content, url):
        soup = BeautifulSoup(content, 'html.parser')

        scrape = Scrape(source=url)
        urlBase = self._getBase(url)

        # url parsing
        scrape.urls = self.parseUrls(urlBase, soup)
        # url parsing
        scrape.files = self.parseFiles(urlBase, soup)

        # imgs
        scrape.imgs = self.parseImgs(urlBase, soup)
        # mp3s
        scrape.mp3s = self.parseMp3s(urlBase, soup)
        # mp4s
        scrape.mp4s = self.parseMp4s(urlBase, soup)

        # htmls
        scrape.htmls = self.parseHtmls(urlBase, soup)
        # txts
        scrape.txts = self.parseTxts(urlBase, soup)
        # pdfs
        scrape.pdfs = self.parsePdfs(urlBase, soup)

        # csvs
        scrape.csvs = self.parseCsvs(urlBase, soup)
        # xmls
        scrape.xmls = self.parseXmls(urlBase, soup)

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

    # Eval

    def info(self):
        for i in self.scrapes:
            i.report()

    # Parse Methods

    def parseUrls(self, urlbase, soup):
        urls = soup.find_all("a")
        urls = [url.get("href") for url in urls]
        urls = [url if not self._hasExtension(url) else None for url in urls]
        urls = self.clean(urls, urlbase)
        return urls

    def parseFiles(self, urlbase, soup):
        urls = soup.find_all("a")
        urls = [url.get("href") for url in urls]
        urls = [url if self._hasExtension(url) else None for url in urls]
        urls = self.clean(urls, urlbase)
        return urls
    #

    def parseImgs(self, urlbase, soup):
        urls = soup.find_all("img")
        urls = [url.get("src") or url.get("data-lazyload") for url in urls]
        urls = self.clean(urls, urlbase)
        return urls

    def parseMp3s(self, urlbase, soup):
        return self.parseFiletype(urlbase, soup, ".mp3")

    def parseMp4s(self, urlbase, soup):
        return self.parseFiletype(urlbase, soup, ".mp4")

    #
    def parseHtmls(self, urlbase, soup):
        return self.parseFiletype(urlbase, soup, ".html")

    def parseTxts(self, urlbase, soup):
        return self.parseFiletype(urlbase, soup, ".txt")

    def parsePdfs(self, urlbase, soup):
        return self.parseFiletype(urlbase, soup, ".pdf")

    #
    def parseCsvs(self, urlbase, soup):
        return self.parseFiletype(urlbase, soup, ".csv")

    def parseXmls(self, urlbase, soup):
        return self.parseFiletype(urlbase, soup, ".xml")

    def parseFiletype(self, urlbase, soup, ext):
        urls = soup.find_all("a")
        urls = [url.get("href") for url in urls]
        urls = [url if self._isType(url, ext) else None for url in urls]
        urls = self.clean(urls, urlbase)
        return urls

    def clean(self, urls, urlbase):
        cleaned = set()
        for url in urls:
            if url:

                if self._isRelativeUrl(url):
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
                writer.writerow([slug, scrape.source, url])

    #
    def saveImages(self):
        print("Saving All Images")
        for scrape in tqdm(self.scrapes):
            print(f"Saving images from: {scrape.source}")
            self.saveImagesForScrape(scrape)

    def saveImagesForScrape(self, scrape):
        if len(scrape.imgs) == 0:
            print(f"No items found from {scrape.source}")
            return
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

    def saveMp3(self):
        print("Saving All MP3 Files")
        for scrape in self.scrapes:
            print(f"Saving mp3 files from: {scrape.source}")
            self.saveFilesForScrape(scrape.source, self._mp3Dir, scrape.mp3s)

    def saveMp4(self):
        print("Saving All MP4 Files")
        for scrape in self.scrapes:
            print(f"Saving mp4 files from: {scrape.source}")
            self.saveFilesForScrape(scrape.source, self._mp4Dir, scrape.mp4s)

    #
    def saveHtml(self):
        print("Saving All Html Files")
        for scrape in self.scrapes:
            print(f"Saving html files from: {scrape.source}")
            self.saveFilesForScrape(scrape.source, self._htmlDir, scrape.htmls)

    def saveTxt(self):
        print("Saving All Text Files")
        for scrape in self.scrapes:
            print(f"Saving text files from: {scrape.source}")
            self.saveFilesForScrape(scrape.source, self._txtDir, scrape.txts)

    def savePdf(self):
        print("Saving All Pdf Files")
        for scrape in self.scrapes:
            print(f"Saving pdf files from: {scrape.source}")
            self.saveFilesForScrape(scrape.source, self._pdfDir, scrape.pdfs)

    #
    def saveCsv(self):
        print("Saving All Csv Files")
        for scrape in self.scrapes:
            print(f"Saving csv files from: {scrape.source}")
            self.saveFilesForScrape(scrape.source, self._csvDir, scrape.csvs)

    def saveXml(self):
        print("Saving All Xml Files")
        for scrape in self.scrapes:
            print(f"Saving xml files from: {scrape.source}")
            self.saveFilesForScrape(scrape.source, self._xmlDir, scrape.xmls)

    def saveFilesForScrape(self, source, direct, urls):
        if len(urls) == 0:
            print(f"No items found from {source}")
            return
        slug = self._slugify(source)
        source = self._slugify(self.url)
        base = source+"/"+direct+"/"+slug
        if not os.path.exists(base):
            os.makedirs(base)
        for file in tqdm(urls):
            filename = self._slugify(file)
            extension = self._getExtension(file)
            try:
                response = urllib.request.urlopen(file)
                with open(base+"/"+filename+extension, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
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

    def _makeAbsolute(self, url, path):
        split_url = urlsplit(url)
        scheme = ""
        if (split_url.scheme != ""):
            scheme = split_url.scheme + "://"
        path = "/"+str(path).strip("/")
        result = scheme + split_url.hostname + path
        return result

    def _getBase(self, url):
        split_url = urlsplit(url)
        clean_url = urlunsplit(
            (split_url.scheme, split_url.netloc, "", "", ""))
        return clean_url

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
        if not url:
            return False
        foundExt = os.path.splitext(url)
        return foundExt[1]

    def _isType(self, url, ext):
        if not url:
            return False
        foundExt = os.path.splitext(url)
        return foundExt[1].lower() == ext

    def _hasExtension(self, url):
        if not url:
            return False
        foundExt = os.path.splitext(url)
        return foundExt[1] != ""

    def _isJson(self, content):
        try:
            json.loads(content)
            return True
        except:
            return False

    def _isXml(self, content):
        try:
            ET.ElementTree(ET.fromstring(content))
            return True
        except:
            return False

    def _isHtml(self, content):
        return bool(BeautifulSoup(content, "html.parser").find() and not self._isXml(content))

    def _isAbsoluteUrl(self, url):
        m = re.search('([a-z0-9]*:|.{0})\/\/.*', str(url))
        return bool(m)

    def _isRelativeUrl(self, url):
        m = re.search('[^\/]+\/[^\/].*$|^\/[^\/].*', url)
        return bool(m)

    def _getUrls(self, content):
        m = re.findall(
            r"((?:[a-z0-9]*:|.{0})\/\/[a-zA-Z0-9\.\/\=\?\&\#\$\-\_\+\!\*\'\(\)\,]*)", content)
        if m:
            return m
        return []


if __name__ == "__main__":
    print("My spidey senses are tingling")

    url = "https://www.google.com/"

    parser = Pyderman(url=url, depth=0)
    parser.run()

    # Print Out Report
    for scrape in parser.scrapes:
        scrape.report()
        for i in scrape.files:
            print(i)

    # GRAPH
    # parser.saveGraph()

    # IMAGES
    # parser.saveImages()
    # MP3
    # parser.saveMp3()
    # MP4
    # parser.saveMp4()

    # HTML
    # parser.saveHtml()
    # TXT
    # parser.saveTxt()
    # PDF
    # parser.savePdf()

    # CSV
    # parser.saveCsv()
    # XML
    # parser.saveXml()
