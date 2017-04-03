
import logging

import requests
import bs4

import utils

logging.basicConfig()
logger = logging.getLogger("mangastream")
logger.setLevel("DEBUG")


def get_url_image(soup_page):
    div_page = soup_page.find("div", attrs={"class": "read_img"})

    if not div_page:
        return None

    url_image = div_page.find("img")["src"]

    if url_image.startswith("//"):
        url_image = "http:" + url_image 

    return url_image


def get_url_next(soup_page):
    div_page = soup_page.find("div", attrs={"class": "read_img"})

    if not div_page:
        return None

    url_next = div_page.find("a")["href"]

    return url_next


def get_chapter(url_chapter):

    logger.info("Downloading chapter under URL '{0}'".format(url_chapter))

    url_next = url_chapter

    # create an in-memory zip-file to store the retrieved images
    fzip = utils.InMemoryZip()

    counter_page = 1
    while True:
        logger.info("Getting page '{0}'".format(url_next))

        # get the page and parse it with `BeautifulSoup`
        response = requests.get(url_next, timeout=60)

        soup_page = bs4.BeautifulSoup(response.content, "lxml")

        # retrieve the image URL
        url_image = get_url_image(soup_page=soup_page)

        # stop if no image was found
        if not url_image:
            break

        logger.info("Getting image '{0}'".format(url_image))

        # retrieve the actual image
        response_image = requests.get(url_image, timeout=60)
        
        # retrieve the `Content-Type` header-value and define the extension
        content_type = response_image.headers["Content-Type"]
        image_extension = content_type.split("/")[-1]

        # name the image through the counter and the mimetype-extension
        fname_image = "{0}.{1}".format(str(counter_page).zfill(3), image_extension)

        logger.info("Writing image '{0}'".format(fname_image))

        # write the retrieved image into the in-memory zip-file
        fzip = fzip.append(fname_image, response_image.content)

        # get the next URL
        url_next_candidate = get_url_next(soup_page=soup_page)

        logger.info("Evaluating URL '{0}' for continuation".format(url_next_candidate))

        # if anything but the last portion of the URL has changed that means we were redirected to the next chapter
        # instead of the next image so halt execution
        if url_next_candidate.endswith(".html"):
            logger.info("URL '{0}' considered part of the chapter. Continuing".format(url_next_candidate))            
            url_next = url_next_candidate
        else:
            logger.info("URLs '{0}' and '{1}' are too disimilar. Stopping".format(url_next, url_next_candidate))
            break

        counter_page += 1

    # return the in-memory zip-file
    return fzip
