<img src="https://github.com/brendenvogt/PYderman/blob/master/resources/pyderman.png?raw=true" width="388"/>


# PYderman
#### Your friendly neighborhood web spider; written in **Python**.
This program scrapes and crawls the website you give it for links and images. It then proceeds to crawl every href url on that site for more images and links. Pyderman does this until it reaches `depth` levels. <br/>
Setting `depth=0` means no crawling, only scraping that current page.<br/>
Setting `depth=1` means scraping and crawling the current page, and the direct links from that page.<br/>
Setting `depth=100` may set your computer on fire. 😂
## Important Notes
Friendly warning, set `depth` to a small number like `depth=0` or `depth=1`, otherwise you risk downloading a LOT of data.<br/>
And be careful which sites you set this loose on.

## Usage 

### Set Start Url
```python
url = "https://www.google.com/"
```
### Create Object and Set Config
```
parser = Pyderman(url=url, depth=1)
```
#### Alternate Declaration
Using the Python [**Urllib**](https://docs.python.org/3/library/urllib.html) Http Client
```
parser = Pyderman(url=url,req="urllib" depth=1)
```
Using the Python [**Requests**](http://docs.python-requests.org/en/master) Http Client
```
parser = Pyderman(url=url,req="requests" depth=1)
```

##### Run
```
parser.run()
```

##### Save Images or Graph
```
#IMAGES
parser.saveImages()	
#GRAPH
parser.saveGraph()
```

## Result 

### Images
<img src="https://github.com/brendenvogt/PYderman/blob/master/resources/imgsScreenshot.png?raw=true"/>

### Graph
<img src="https://github.com/brendenvogt/PYderman/blob/master/resources/graphScreenshot.png?raw=true"/>
