import bs4 as bs
import urllib.request
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Spider():

    def __init__(self, url):
        self.url = url

    def getStaticSoup(self):
        # START option 1 Requests
        # content = requests.get(self.url).text
        # END option 1

        # START option 2 urllib.request
        content = urllib.request.urlopen(self.url).read()
        # END option 2

        soup = bs.BeautifulSoup(content, "html.parser")
        return soup

    def getDynamicSoup(self):
        # START option 1: Firefox
        # driver = webdriver.Firefox() # opens firefox
        # End option 1

        # START option 2: PhantomJS
        # driver = webdriver.PhantomJS() # deprecated
        # END option 2

        # START option 3: Headless Chromium
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(self.url)
        # END option 3

        content = driver.page_source
        soup = bs.BeautifulSoup(content, "html.parser")
        driver.close()
        return soup


if __name__ == "__main__":
    url = "https://www.iherb.com"
    x = Spider(url)

    # Static Content
    # print(x.getStaticSoup())

    # Dynamic Content
    print(x.getDynamicSoup())
