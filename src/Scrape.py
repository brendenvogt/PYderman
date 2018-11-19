
class Scrape():

    def __init__(self, source="", urls=[], files=[], htmls=[], txts=[], pdfs=[], csvs=[], xmls=[], imgs=[], mp3s=[], mp4s=[]):
        self.source = source
        self.urls = urls
        self.files = files
        # media
        self.imgs = imgs
        self.mp3s = mp3s
        self.mp4s = mp4s
        # standard
        self.htmls = htmls
        self.txts = txts
        self.pdfs = pdfs
        # data
        self.csvs = csvs
        self.xmls = xmls

    def report(self):
        print(f"Scrape Report from: {self.source}")
        for k, v in self.__dict__.items():
            if k in ["self", "source"]:
                continue
            print(f"- number of {k}: {len(v)}")
