import scrapy


class IbitsSpider(scrapy.Spider):
    name = "ibits"
    allowed_domains = ["ibits.ca"]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070213 BonEcho/2.0.0.2pre',
        'ROBOTSTXT_OBEY': False
    }

    start_urls = ["https://ibits.ca/careers/?selected_location=regina"]

    def parse(self, response):
        joblist_container = response.xpath('//div[@class="v2 sjb-job-887"]')
        for job in joblist_container:
            company = "iBiTS"
            job_title = job.xpath(".//span[@class='job-title']/text()").get()
            location = job.xpath(".//div[@class='job-location']/text()").get()
            link = job.xpath(".//a/@href").get()

            yield{
                'company': company,
                'job_title': job_title,
                'location': location,
                'link': link,
            }