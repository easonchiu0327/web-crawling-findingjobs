# Saskatchewan IT Job Scraper

This project is a simple web scraping bot, combining **Scrapy** and **Selenium** that collects job listings from multiple websites and save them into a **SQL** Server database.

# Result demo
## jsonl file
<img width="1603" height="882" alt="image" src="https://github.com/user-attachments/assets/fb98b0c2-b4d8-4658-821b-ab27030bd655" />

## SQL
<img width="1427" height="863" alt="image" src="https://github.com/user-attachments/assets/07f8ccb6-e117-4bcb-b14c-3dd88eb56bb8" />

# Testing link
[Vendasta's spider demo](https://colab.research.google.com/drive/1uemPB5HmvLIzSF3dtpm_e4jCEPshVXqF?usp=sharing)

[7shifts's spider demo](https://colab.research.google.com/drive/1vZ4cIvEO-kjCf9qIlYFloHHh3evQ5RI7#scrollTo=xLYaMbypM3kD)

This spider integrates the OpenAI API to analyze job description pages, extracting the job category, required skills, years of experience, and whether Canadian citizenship or permanent residency is required.


## Features
- Scrapes job postings from various companies
- Outputs results into a SQL Server database
- Easy to extend with more spiders

## How to run
Run a specific spider on terminal:
```bash
scrapy crawl spider_name
```
Or run all spiders on terminal:
```bash
python run_all_spiders.py
```

## Strategy Overview

1. Scrapy is used for websites where job postings are in the static HTML.

2. Selenium is used for sites that load content dynamically with JavaScript.

3. Selenium + Scrapy.Selector is used for scraping job data from a JavaScript-powered page.

## Key Points:

1. Handling Dynamic Filters/Categories/Label with JavaScript Clicks
   
    In some job boards, filters/categories/labels (e.g., by location or department) are rendered dynamically and require user interaction to apply. Standard `.click()` methods in Selenium often fail due to overlays, animations, or incomplete rendering. To solve this, the spider uses **JavaScript-based clicking** with `driver.execute_script()`.

2. Scrapy Selector for Parsing
   
    Once the page is rendered, Scrapy's `Selector` is used to parse HTML using XPath, instead of BeautifulSoup.

3. XPath for Extraction
   
    XPath expressions are used to target job titles, locations, and links.

4. Extracting Data Using `yield`
   
    Using **yield** to return extracted data **one item at a time** from our spider. This is different from `return`, which ends the function immediately.

### ⚠️ **Disclaimer**
This project is for educational use only. 
Always review and respect the robots.txt and terms of service of any website you scrape.

### ⚠️ **Note:** 
This project attempts to collect IT-related job postings, some non-IT roles may appear due to inconsistencies on job boards.

There is a temporary solution on 7shifts's spider demo.
