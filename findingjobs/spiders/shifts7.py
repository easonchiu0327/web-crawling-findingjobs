import scrapy
from selenium import webdriver
from scrapy.selector import Selector # Allows using XPath/Selectors on raw HTML like Scrapy
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class A7shiftsSpider(scrapy.Spider):
    name = "7shifts"
    allowed_domains = ["www.7shifts.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,  # Delay between requests to avoid overloading the server
    }
    start_urls = ["https://www.7shifts.com/careers/"]

    def parse(self, response):
        #set up selenium
        # 1️⃣ --- Setup Selenium Chrome Driver ---
        # the path of where the chrome driver is
        path = r'C:\Users\eason\webscraping_online course\chromedriver-win64\chromedriver.exe'
        service = Service(executable_path=path)
        # 2️⃣ --- Configure Chrome options --
        options = Options()
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--headless=new")
        # 3️⃣ --- Launch Chrome browser with Selenium ---
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.start_urls[0])
        time.sleep(20) # Wait for JavaScript to load content
        try:
            # Now get the HTML after filtering
            # 5️⃣ --- Get the full rendered HTML after JavaScript has run ---
            html = driver.page_source
            # 6️⃣ --- Use Scrapy's Selector to parse the HTML ---
            # scrapy Selector is then used to parse the final HTML returned by Selenium.
            sel = Selector(text=html)

            # using scrapy
            job_container = sel.xpath("//div[@class='space-y-10 pt-20 px-16']//div[@class='space-y-4']/div")
            for job in job_container:
                company = "7shifts"
                job_title = job.xpath(".//a/h3/text()").get()
                location = job.xpath(".//a/p/text()").get()
                link = job.xpath(".//a/@href").get()

                yield{
                    'Company': company,
                    'Job title': job_title,
                    'Location': location,
                    'Link': link,
                }
        except Exception as e:
            self.logger.error(f"Dropdown interaction failed: {e}")
        finally:
            driver.quit()