import scrapy


class HorizonSpider(scrapy.Spider):
    name = "horizon"
    allowed_domains = ["careers.topechelon.com"]
    start_urls = ["https://careers.topechelon.com/portals/df6d26b0-e9b1-412b-8aa2-50f61da6a415/jobs?location=Saskatchewan"]

    def parse(self, response):
        joblist_container = response.xpath('//a[@class="listing--link"]')
        for job in joblist_container:
            company = "Horizon"
            job_title = job.xpath(".//div[@class='listing__title']/text()").get()
            location = job.xpath(".//div[@class='listing__loc']/text()").get()
            link = job.xpath("./@href").get()

            yield{
                "Company": company,
                "Job_title": job_title,
                "Location": location,
                #getting the absolute url
                "Link": response.urljoin(link),
            }