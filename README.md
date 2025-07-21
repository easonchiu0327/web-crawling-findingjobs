# Find the current opening jobs in Saskatchewan

This project is a simple web scraping bot, combinding Scrapy and Selenium that collects job listings from multiple websites and save them to a SQL Server database.

# Features
- Scrapes job postings from various companies
- Outputs results in JSONL format
- Includes a script to push data to SQL Server
- Easy to extend with more spiders

# How to run
Run a specific spider on terminal:
```bash
scrapy crawl spider_name
```
Or run all spiders on terminal:
```bash
python run_all_spiders.py
```

## Implementation Details

This project uses both **Scrapy** and **Selenium** to handle different types of job websites, depending on how the job data is loaded.

### Strategy Overview

- **Scrapy** is used for websites where job postings are in the static HTML.
- **Selenium** is used for sites that load content dynamically with JavaScript.
- **Selenium + Scrapy.Selector** is used for scraping job data from a JavaScript-powered page.

#### Key Points:

- **Handling Dynamic Filters/Categories/Label with JavaScript Clicks**
In some job boards, filters/categories/labels (e.g., by location or department) are rendered dynamically and require user interaction to apply. Standard `.click()` methods in Selenium often fail due to overlays, animations, or incomplete rendering. To solve this, the spider uses **JavaScript-based clicking** with `driver.execute_script()`.

- **Scrapy Selector for Parsing**
Once the page is rendered, Scrapy's `Selector` is used to parse HTML using XPath, instead of BeautifulSoup.

- **XPath for Extraction**
XPath expressions are used to target job titles, locations, and links.

- **Extracting Data Using `yield`**
Using **yield** to return extracted data **one item at a time** from our spider. This is different from `return`, which ends the function immediately

# ⚠️ **Disclaimer**
This project is for educational use only. 
Always review and respect the robots.txt and terms of service of any website you scrape.

# ⚠️ **Note:** 
This project attempts to collect IT-related job postings, but due to inconsistencies on job boards, some non-IT roles may appear in the results. I will figure it out and slove this issue in the furure.
