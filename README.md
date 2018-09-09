<img src="https://github.com/brendenvogt/Spyderman/blob/master/NOTES/spyderman.png?raw=true" width="388"/>


# sPYderman
#### Your friendly neighborhood web spider; written in **Python**.
This program scrapes and crawls the website you give it for links and images. It then proceeds to crawl every href url on that site for more images and links. Spyderman does this until it reaches `depth` levels. <br/>
Setting `depth=0` means no crawling, only scraping that current page.<br/>
Setting `depth=1` means scraping and crawling only the direct links from that page.<br/>
Setting `depth=100` may set your computer on fire.
## Important Notes
Friendly warning, set `depth` to a small number like `depth=0` or `depth=1`, otherwise you risk downloading a LOT of data.<br/>
And be careful which sites you set this loose on.

## Usage 

##### Set Start Url
```python
url = "https://www.google.com/"
```
##### Create Object and Set Config
```
parser = Spyderman(url=url,req="requests", depth=1)

# req="requests" uses the python request http client
# req="urllib" uses the python urllib http client
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
