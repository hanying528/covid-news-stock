import scrapy

BASE_URL = "https://search.api.cnn.io"


class CNNNews(scrapy.Spider):
    name = "CNNNews"
    start = 1
    start_urls = [BASE_URL + "/content?q=covid&size=100"]

    def parse(self, response):
        # Get all the news summary from the current page
        results = response.json()['result']
        headlines = []
        dates = []
        for res in results:
            headline = res['headline']
            # Only if headline contains the following keywords
            if headline:
                if 'covid' in headline.lower() or 'coronavirus' in headline.lower() \
                        or 'pandemic' in headline.lower() or 'sars' in headline.lower()\
                        or 'vaccination' in headline.lower() or 'virus' in headline.lower():
                    dt = res['firstPublishDate'][:10]  # we only need the date
                    dates.append(dt)
                    headlines.append(headline)
        page = response.url.split("/")[-2]
        filename = f'{self.name}-{page}.txt'

        # Save to file (append mode)
        with open(filename, 'a') as f:
            for dt, headline in zip(dates, headlines):
                f.write(f"{dt}, {headline}\n")
        self.log(f'Updated file {filename}')

        # Next page
        self.start += 100
        next_page_url = BASE_URL + f"/content?q=covid&size=100&from={self.start}"
        self.log("Crawling next page...")
        yield scrapy.Request(next_page_url, callback=self.parse)
