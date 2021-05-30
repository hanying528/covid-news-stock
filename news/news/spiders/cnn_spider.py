import scrapy

BASE_URL = "https://search.api.cnn.io"


class CNNNews(scrapy.Spider):
    name = "CNNNews"
    start = 1
    start_urls = [BASE_URL + "/content?q=covid-19&sort=newest&size=100"]

    def parse(self, response):
        # Get all the news summary from the current page
        results = response.json()['result']
        headlines = []
        for res in results:
            headlines.append(res['headline'])
        page = response.url.split("/")[-2]
        filename = f'{self.name}-{page}.txt'

        # Save to file (append mode)
        with open(filename, 'a') as f:
            for headline in headlines:
                f.write("%s\n" % headline)
        self.log(f'Updated file {filename}')

        # Next page
        self.start += 100
        next_page_url = BASE_URL + f"/content?q=covid-19&sort=newest&size=100&from={self.start}"
        self.log("Crawling next page...")
        yield scrapy.Request(next_page_url, callback=self.parse)
