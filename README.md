<img src="https://github.com/brendenvogt/PYderman/blob/master/resources/pyderman.png?raw=true" width="388"/>


# PYderman
#### Your friendly neighborhood web spider; written in **Python**.
This program scrapes and crawls the website you give it for links and files. It then proceeds to crawl every href url on that site for more links and files. Pyderman does this until it reaches `depth` levels. <br/>
Pyderman supports image files, .mp3, .mp4, .html, .txt, .pdf, .csv, and .xml files.<br/>
Setting `depth=0` means no crawling, only scraping that current page.<br/>
Setting `depth=1` means scraping and crawling the current page, and the direct links from that page.<br/>
Setting `depth=100` may set your computer on fire. 😂
* Adding support for json and xml parsing
#### Roadmap for the future...
* Make a crawler to find api endpoints that return xml or json, then auto document them.
* refine crawler to search any type of document type (html, json, xml, text, etc)
## Important Notes
Friendly warning, set `depth` to a small number like `depth=0` or `depth=1`, otherwise you risk downloading a LOT of data.<br/>
And be careful which sites you set this loose on.

## Usage 

### Import
```python
from Pyderman import Pyderman
```
### Set Start Url
```python
url = "https://www.google.com/"
```
### Create Object and Set Config
```python
parser = Pyderman(url=url, depth=1)
```
#### Alternate Declaration
Using the Python [**Urllib**](https://docs.python.org/3/library/urllib.html) Http Client
```python
parser = Pyderman(url=url,req="urllib" depth=1)
```
Using the Python [**Requests**](http://docs.python-requests.org/en/master) Http Client
```python
parser = Pyderman(url=url,req="requests" depth=1)
```

##### Run
```python
parser.run()
```

##### Save Images or Graph
```python
#IMAGES
parser.saveImages()	

#GRAPH
parser.saveGraph()

##MP3
parser.saveMp3()

##MP4
parser.saveMp4()

##HTML
parser.saveHtml()

##TXT
parser.saveTxt()

##PDF
parser.savePdf()

##CSV
parser.saveCsv()

##XML
parser.saveXml()
```

## Result 

### Images
<img src="https://github.com/brendenvogt/PYderman/blob/master/resources/imgScreenshot.png?raw=true"/>


### Graph
<img src="https://github.com/brendenvogt/PYderman/blob/master/resources/graphScreenshot.png?raw=true"/>
