import scrapy


class OpensailSpider(scrapy.Spider):
    name = "opensail"
    allowed_domains = ["www.opensail.com"]
    start_urls = ["https://www.opensail.com/company/careers"]

    def parse(self, response):
        job_ocntainer = response.xpath('//div[@role="listitem"]')
        for job in job_ocntainer:
            company = "Opensail"
            job_title = job.xpath('.//h1[@class="heading-46"]/text()').get()
            location = job.xpath('.//h1[@class="heading-47"]/text()').get()
            link = job.xpath('.//a/@href').get()

            yield {
                "Company": company,
                "Job_title": job_title,
                "Location": location,
                "Link": response.urljoin(link),
            }