# PyterParker
#### Your friendly neighborhood web spider; written in **Python**.
This program scrapes and crawls the website you give it for links and images. It then proceeds to search every href link that it found for more images and links. PyterParker does this until it reaches `depth` levels. 
Setting `depth=0` means no crawling, only scraping the provided `url`
Setting `depth=1` means scrape and crawl only the direct links found on page

## Important Notes
Friendly warning, set `depth` to a small number like `depth=0` or `depth=1`, otherwise you risk downloading a LOT of data.
And be careful which sites you set this loose on.

## Usage 

##### Set Start Url
```python
url = "https://www.google.com/"
```
##### Create Object and Set Config
```
parser = PyterParker(url=url,req="requests", depth=1)

# req="requests" uses the python request http client
# req="urllib" uses the python urllib http client

parser.run()

```

##### Save Images or Graph
```
#IMAGES
parser.saveImages()	
#GRAPH
parser.saveGraph()

```
