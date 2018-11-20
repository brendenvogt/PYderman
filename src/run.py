
from Pyderman import Pyderman

if __name__ == "__main__":

    url = "https://www.brendenvogt.com/"

    p = Pyderman(url=url, depth=0)

    p.run()

    # p.saveImages()

    # p.saveGraph()

    p.info()
