
from Pyderman import Pyderman

if __name__ == "__main__":

    # url = "https://www.brendenvogt.com/"
    url = "https://www.iherb.com/ugc/api/product/11242"

    p = Pyderman(url=url, depth=0)

    p.run()

    p.saveImages()

    p.info()
