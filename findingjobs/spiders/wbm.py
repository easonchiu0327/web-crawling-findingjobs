import scrapy


class WbmSpider(scrapy.Spider):
    name = "wbm"
    allowed_domains = ["www.wbm.ca"]
    start_urls = ["https://www.wbm.ca/careers/current-postings/?location=saskatchewan"]

    def parse(self, response):
        #a container for each job
        joblist_container = response.xpath('//a[@class="career"]')
        for job in joblist_container:
            company = "WBM"
            job_title = job.xpath('.//h2/text()').get()
            location = job.xpath('.//h3/text()').get()
            link = job.xpath('./@href').get()

            yield{
                'company': company,
                'job_title': job_title,
                'location': location,
                'link': link,
            }
