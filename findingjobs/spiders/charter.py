import scrapy
from selenium import webdriver
from scrapy.selector import Selector # Allows using XPath/Selectors on raw HTML like Scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from urllib.parse import urljoin # To build absolute URLs from relative paths
import time

#Flow Recap:
# When a website loads content dynamically using JavaScript (like filtering jobs by location), Scrapy can't see that — because it doesn't run JavaScript.
# That's why I use scrapy + selenium in this case
# Selenium → Interacts with page (JavaScript filters, dropdowns, etc.)
# driver.page_source → Takes a snapshot of the final, rendered HTML
# Selector(text=html) → Gives that snapshot to Scrapy for XPath/CSS parsing
# Scrapy parsing → Cleanly extracts structured job data


class CharterSpider(scrapy.Spider):
    name = "charter"
    allowed_domains = ["charter-telecom-inc.breezy.hr"]
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5, # Delay between requests to avoid overloading the server
    }
    start_urls = ["https://charter-telecom-inc.breezy.hr/"]

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
        time.sleep(5)
        try:
            # dealing with the dropdown
            location_dropdown = Select(driver.find_element(By.CLASS_NAME, 'locations'))
            location_dropdown.select_by_visible_text('SK, CA')
            # it needs some time to load the page
            time.sleep(5)
            # Now get the HTML after filtering
            # 5️⃣ --- Get the full rendered HTML after JavaScript has run ---
            html = driver.page_source
            # 6️⃣ --- Use Scrapy's Selector to parse the HTML ---
            # scrapy Selector is then used to parse the final HTML returned by Selenium.
            sel = Selector(text=html)

            # using scrapy
            job_container = sel.xpath('//ul[@class="position-wrap pad-b-50"]')
            for job in job_container:
                company = "Charter"
                job_title = job.xpath('.//h2/text()').get()
                location = job.xpath('(.//span)[3]/text()').get()
                link = job.xpath('./li[@class="position-actions"]/a/@href').get()

                yield {
                    "company": company,
                    "Job title": job_title,
                    "location": location,
                    "link": urljoin(self.start_urls[0], link),  # Convert relative link to full URL
                }
        except Exception as e:
            self.logger.error(f"Dropdown interaction failed: {e}")
            driver.quit()
        finally:
            driver.quit()


