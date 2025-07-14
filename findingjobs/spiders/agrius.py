import scrapy


class AgriusSpider(scrapy.Spider):
    name = "agrius"
    allowed_domains = ["www.agrius.ca"]
    start_urls = ["https://www.agrius.ca/?page_id=638"]

    def parse(self, response):
        job_container = response.xpath("//em")
        for job in job_container:
            company = "AGRIUS"
            job_title = job.xpath("./strong/text()").get()
            location = "Regina"
            link = job.xpath("./a/@href").get()

            yield{
                "Company": company,
                #\xa0 is the non-breaking space (NBSP).
                "Job_title": job_title.replace('\xa0', ' ').strip() if job_title else None,
                "Location": location,
                "Link": link,
            }
