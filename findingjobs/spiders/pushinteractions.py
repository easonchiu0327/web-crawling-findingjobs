import scrapy


class PushinteractionsSpider(scrapy.Spider):
    name = "pushinteractions"
    allowed_domains = ["pushinteractions.com"]
    start_urls = ["https://pushinteractions.com/careers/"]

    def parse(self, response):
        job_container = response.xpath("//div[@class='div-block-40']")
        for job in job_container:
            company = "PushInteractions"
            job_title = job.xpath(".//h2/text()").get()
            # the pattern is:Start at position 2. Then select every 3rd item (2, 5, 8, 11, ...)
            location = job.xpath("(.//div[@class='text-block-12'])[(position()-2) mod 3 = 0]/text()").get()
            link = job.xpath(".//a[@class='button w-button']/@href").get()

            yield{
                "company": company,
                # remove \n (newline characters) (and other unwanted whitespace) using .strip()
                "job_title": job_title.strip() if job_title else None,
                "location": location.strip() if location else None,
                "link": response.urljoin(link),
            }