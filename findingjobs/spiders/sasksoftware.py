import scrapy


class SasksoftwareSpider(scrapy.Spider):
    name = "sasksoftware"
    allowed_domains = ["www.sasksoftware.com"]
    start_urls = ["https://www.sasksoftware.com/careers/"]

    def parse(self, response):
        job_container = response.xpath('//div[@class="content"]')
        for job in job_container:
            company = "SaskSoftware"
            job_title = job.xpath('.//h3/text()').get()
            location = "N/A"
            link = self.start_urls[0]

            yield{
                "Company": company,
                "Job Title": job_title,
                "Location": location,
                "link": link,

            }