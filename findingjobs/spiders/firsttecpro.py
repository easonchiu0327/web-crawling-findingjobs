import scrapy


class FirsttecproSpider(scrapy.Spider):
    name = "firsttecpro"
    allowed_domains = ["www.firsttecpro.com"]
    start_urls = ["https://www.firsttecpro.com/careers/"]

    def parse(self, response):
        job_container = response.xpath("//div[@class='box']")
        for job in job_container:
            company = "FirstTeCPro"
            job_title = job.xpath(".//h3/text()").get()
            # position() mod 4 = 0 selects every 4th element.
            location = job.xpath("(.//span)[position() mod 4 = 0]/text()").get()
            link = job.xpath(".//a[@class='button']/@href").get()

            yield{
                "Company": company,
                "Job_title": job_title,
                "Location": location.strip() if location else None,
                "Link": link,
            }