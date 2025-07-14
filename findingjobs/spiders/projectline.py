import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class ProjectlineSpider(scrapy.Spider):
    name = "projectline"
    allowed_domains = ["www.projectline.ca", "careers.risepeople.com"]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,  # <-- this is what allows crawling forbidden pages,  bypass the robots.txt blocking issue.
        'DOWNLOAD_DELAY': 1.5,
    }

    start_urls = ["https://www.projectline.ca/company/careers"]

    def parse(self, response):
        joblist_container = response.xpath("//div[contains(@class, 'content-card  content-card--with-link content-card--no-img-just-icon')]")
        for job in joblist_container:
            company = "Projectline"
            job_title = job.xpath("./a/span/text()").get()
            link = job.xpath("./a/@href").get()

            # yield{
            #     'company': company,
            #     'job_title': job_title,
            #     'link': link,
            # }
            absolute_url = response.urljoin(link)
            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse_link,
                meta={"Company": company, "Job_title": job_title, "link": link},
                # Scrapy ignored a request because it had already visited that URL earlier in the crawl.
                # This tells Scrapy: “Yes, even if you saw this URL before, crawl it again.”
                dont_filter=True
            )

    # Getting data inside the "link" website
    def parse_link(self, response):
        company = response.request.meta["Company"]
        job_title = response.request.meta["Job_title"]
        link = response.request.meta["link"]
        #the content is dynamically rendered by JavaScript (likely using Angular, judging by _ngcontent-*). Scrapy cannot see JavaScript-rendered content because it does not execute JavaScript.
        #so we need selenium here

        #set up selenium

        # the path of where the chrome driver is
        path = r'C:\Users\eason\webscraping_online course\chromedriver-win64\chromedriver.exe'
        service = Service(executable_path=path)
        # the driver here is for scraping the website
        # Create the driver using Service
        options = Options()
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(service=service, options=options)
        try:
            driver.get(link)
            time.sleep(5)
            location = driver.find_element(By.XPATH, "(//span[@id='icon-text-modal'])[1]").text
            yield {
                "Company": company,
                "Job_title": job_title,
                "Location": location,
                "Link": link,
            }

        except:
            location = "N/A"
        finally:
            driver.quit()





