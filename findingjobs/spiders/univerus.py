import scrapy
from selenium import webdriver
from scrapy.selector import Selector # Allows using XPath/Selectors on raw HTML like Scrapy
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from urllib.parse import urljoin # To build absolute URLs from relative paths
import time

# the location need to be fixed!

class UniverusSpider(scrapy.Spider):
    name = "univerus"
    allowed_domains = ["univerus.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,  # Delay between requests to avoid overloading the server
        'USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070213 BonEcho/2.0.0.2pre',
        'ROBOTSTXT_OBEY': False
    }
    start_urls = ["https://univerus.com/about-us/search-jobs/"]

    def parse(self, response):
        # set up selenium
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
            # check the label
            province_label = driver.find_element(By.XPATH, '//label[@for="stateCheck2"]')
            province_label.click()
            # it needs some time to load the page
            time.sleep(5)
            # Now get the HTML after filtering
            # 5️⃣ --- Get the full rendered HTML after JavaScript has run ---
            html = driver.page_source
            # 6️⃣ --- Use Scrapy's Selector to parse the HTML ---
            # scrapy Selector is then used to parse the final HTML returned by Selenium.
            sel = Selector(text=html)

            # using scrapy
            job_container = sel.xpath('(//div[@class="mindscope paginate"])[position() < last()]')
            for job in job_container:
                company = "Univerus"
                job_title = job.xpath('.//h5/a/text()').get()
                location = job.xpath('(.//p)[(position() - 1) mod 3 = 0]/text()').get()
                link = job.xpath('.//h5/a/@href').get()

                yield {
                    'Company': company,
                    'Job_title': job_title,
                    'Location': location,
                    'Link': link,
                }
        except Exception as e:
            self.logger.error(f"check label interaction failed: {e}")
        finally:
            driver.quit()



