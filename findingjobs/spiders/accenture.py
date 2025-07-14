import scrapy
from selenium import webdriver
from scrapy.selector import Selector # Allows using XPath/Selectors on raw HTML like Scrapy
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By


class AccentureSpider(scrapy.Spider):
    name = "accenture"
    allowed_domains = ["www.accenture.com"]
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,  # Delay between requests to avoid overloading the server
        'ROBOTSTXT_OBEY': False
    }
    start_urls = ["https://www.accenture.com/ca-en/careers/jobsearch?jk="]

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
        time.sleep(10) # Wait for JavaScript to load content
        try:
            # dealing with the filter
            filter_results = driver.find_element(By.XPATH,"//div[@class='jobsearchfilter']//button")
            #when Selenium tries to click on an element (likely your "Update" button), something is blocking it—like a popup, overlay, sticky header, or the page isn't fully loaded or scrolled.
            # Click using JavaScript
            driver.execute_script("arguments[0].click();", filter_results)
            time.sleep(3)
            location_filter = driver.find_element(By.XPATH,"//div[@data-filter-id='City']")
            driver.execute_script("arguments[0].click();", location_filter)
            time.sleep(3)
            click_saskatchewan = driver.find_element(By.XPATH,"//span[@class='cmp-form-options__field-description cmp-text' and contains(text(), 'Saskatchewan')]")
            driver.execute_script("arguments[0].click();", click_saskatchewan)
            time.sleep(3)
            click_update = driver.find_element(By.XPATH,"//div[@class='button cmp-button--primary-white cmp-job-search-filtering__update']/button")
            driver.execute_script("arguments[0].click();", click_update)
            time.sleep(3)

            # Now get the HTML after filtering
            # 5️⃣ --- Get the full rendered HTML after JavaScript has run ---
            html = driver.page_source
            # 6️⃣ --- Use Scrapy's Selector to parse the HTML ---
            # scrapy Selector is then used to parse the final HTML returned by Selenium.
            sel = Selector(text=html)

            # using scrapy
            location = sel.xpath("//div[@class='selected-filter-container__progressive-button']/text()").get()
            job_container = sel.xpath("//div[@class='cmp-teaser card']/a")
            for job in job_container:
                company = "Accenture"
                job_title = job.xpath(".//h3/text()").get()
                location = location.strip() if location else None
                link = job.xpath("./@href").get()

                # Only yield if job_title and link are valid
                if job_title and link:
                    item = {
                        'Company': company,
                        'Job_title': job_title,
                        'Location': location,
                        'Link': link,
                    }
                    self.logger.info(f"Extracted job: {item}")
                    yield item
        except Exception as e:
            self.logger.error(f"Dropdown interaction failed: {e}")
        finally:
            driver.quit()


