
import begin

import scraper


@begin.subcommand
def url(url, fname_output):
    fzip = scraper.get_chapter(url_chapter=url)
    fzip.writetofile(fname_output)


@begin.start
def main():
    pass
