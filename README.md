# mangatown-downloader

This is a simple collection of scripts that allows one to download a [MangaTown](http://mangatown.com/) manga chapter by providing the URL to the first page of the chapter.

The script scrapes the HTML source of the page, retrieves the link to the current image as well as the URL that image points to, i.e., the next page of the chapter. It then saves every page image into an in-memory zip-file and continues this process until the end of the chapter.

## Usage

The `mangatown.py` module acts as a CLI interface to the code under `scraper.py` and can be used to download a single chapter from a provided URL.

Download a single chapter through its URL and write it to a `.zip` file:

    python mangatown.py url http://www.mangatown.com/manga/shen_yin_wang_zuo/c111/
