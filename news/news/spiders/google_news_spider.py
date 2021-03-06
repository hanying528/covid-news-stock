import sys

from bs4 import BeautifulSoup
import scrapy

BASE_URL = "https://www.google.com"


class GoogleNews(scrapy.Spider):
    name = "GoogleNews"
    # Set start date to 20219/12/01
    start_urls = [BASE_URL + "/search?q=COVID-19&tbm=nws&lr=lang_en&hl=en&cd_min%3A12%2F01%2F2019%2Ccd_max%3A"]

    def parse(self, response):
        # Get all the news summary from the current page
        soup = BeautifulSoup(response.text, "html.parser")
        summaries = []
        divs = soup.findAll("div", {"class": "BNeawe vvjwJb AP7Wnd"})
        for div in divs:
            summaries.append(div.text)
        page = response.url.split("/")[-2]
        filename = f'{self.name}-{page}.txt'

        # Save to file (append mode)
        with open(filename, 'a') as f:
            for summary in summaries:
                f.write("%s\n" % summary)
        self.log(f'Updated file {filename}')

        # Find next page
        try:
            next_page_url = BASE_URL + soup.findAll("a", {"aria-label": "Next page"})[0]['href']
        except Exception:
            sys.exit("Error when finding next page. Terminating...")
        self.log("Crawling next page...")
        yield scrapy.Request(next_page_url, callback=self.parse)
