# Saskatchewan IT Job AI-Scraper

This project is a web scraping bot combining Scrapy and Selenium, enhanced with OpenAI API for analyzing job descriptions.
It collects IT-related job listings from multiple websites, enriches them with **AI**, and saves results into a SQL Server database.

# Skills
Python, OpenAI API, Scrapy, Selenium, XPath, Prompt, JSONL, SQL Server

# SQL Result demo
<img width="1526" height="781" alt="image" src="https://github.com/user-attachments/assets/0b293f93-c24e-4588-a67e-2baf1dd5ff6b" />

# Testing link
[Vendasta's spider demo](https://colab.research.google.com/drive/1uemPB5HmvLIzSF3dtpm_e4jCEPshVXqF?usp=sharing)

- A demonstration spider built with Scrapy for structured HTML parsing and Selenium for rendering JavaScript-powered content.
It uses ChromeDriver to automate a headless Chrome browser, navigate the site, handle dynamic content loading, and interact with job listing elements before passing the HTML to Scrapy’s Selector for precise data extraction using XPath for job title, location and job description link.

[7shifts's spider demo](https://colab.research.google.com/drive/1vZ4cIvEO-kjCf9qIlYFloHHh3evQ5RI7#scrollTo=xLYaMbypM3kD)

- A more advanced spider that integrates the OpenAI API to enrich scraped job postings.
For each job detail page, it uses Selenium to load and extract the main body text, then sends it to the AI for structured analysis — automatically identifying the job category, top skills required, years of experience, and whether Canadian citizenship or permanent residency is explicitly required.


## Features
- Scrapes job postings from multiple companies
- Detects static HTML and JavaScript-rendered job boards automatically
- Using AI to identify each job into a category from a fixed list
- Using AI to extracts Skills, Years of experience, and Canadian PR requirement from job descriptions
- Saves output into enriched .jsonl files and SQL Server database
- Designed to be easily extendable with more spiders and future .Net framwork

## Strategy Overview
### This project uses a three-stage approach:
- Collecting job listings using Scrapy/Selenium.
- Enriching job listings with calling OpenAI API.
- Saving enriched job listings into SQL Server.

### Stage 1: Scraping

1. Scrapy
   - Used for websites where job postings are embedded directly in the static HTML.
   - Fast and lightweight since it doesn’t need a browser.
2. Selenium
   - Used for sites that load job postings dynamically with JavaScript.
3. Selenium + Scrapy.Selector
   - Renders pages with Selenium, then uses Scrapy’s Selector for fast and flexible parsing via XPath.
     
### Stage 2: AI-Powered Enrichment

1. Job Category Identification
   - Sends all job titles in one batch to OpenAI (gpt-5-nano).
   - Returns exactly one category per job from a fixed list (Data, Developer, QA, Analyst, etc.).
2. Job Description Analysis
   - Visits each job’s detail page using Selenium.
   - Extracts all visible text from main, article, or body.
   - Sends text to OpenAI (gpt-4o-mini) with instructions to return a a strict JSON file

### Stage 3: Load data into SQL

1. File Selection
   - Automatically picks the most recent enriched JSONL file from the output directory.
   - Skips previously enriched files to avoid duplicate processing.
2. Database Preparation
   - Connects to Microsoft SQL Server using pyodbc with Windows Authentication.
   - Attempts to TRUNCATE TABLE before inserting new data for a clean slate.
3. Data Insertion
   - Reads the JSONL file line-by-line to handle large datasets without overloading memory.
   - Inserts data into the target table.
   - Ensures all fields are trimmed to remove extra whitespace before insertion.

## Key Points:

1. Handling Dynamic Filters/Categories/Label with JavaScript Clicks
   
    - In some job boards, filters/categories/labels (e.g., by location or department) are rendered dynamically and require user interaction to apply.
    - Standard `.click()` methods in Selenium often fail due to overlays, animations, or incomplete rendering.
    - To solve this, the spider uses **JavaScript-based clicking** with `driver.execute_script()`.

2. Scrapy Selector for Parsing
   
    - Once the page is rendered, Scrapy's `Selector` is used to parse HTML using XPath, instead of BeautifulSoup.

3. XPath for Extraction
   
    - XPath expressions are used to target job titles, locations, and links.

4. Extracting Data Using `yield`
   
    - Using **yield** to return extracted data **one item at a time** from our spider.
    - This is different from `return`, which ends the function immediately.

5. Batch Processing for AI

   - Job Category Identification: All job titles are sent in a single API request to OpenAI’s gpt-5-nano model for faster processing and reduced cost.

   - Job Description Analysis: Each job description is processed individually because it requires navigating to the job’s detail page and analyzing the unique content.

   - This enrichment uses OpenAI’s text-generation API via the responses.create() method: (more detail at [Text generation OpenAI API](https://platform.openai.com/docs/guides/text))
   ```python
   from openai import OpenAI
   client = OpenAI()
   
   response = client.responses.create(
       model="gpt-5",
       input="Write a one-sentence bedtime story about a unicorn."
   )

   print(response.output_text)
   ```


7. SQL Server Storage

   - Once enriched, jobs are inserted into an SSMS table with properly sized NVARCHAR columns to prevent truncation.

## Requirements
### Python Packages
Install dependencies:
```bash
pip install -r requirements.txt
```

### ChromeDriver
- Download from [ChromeDriver](chromedriver.chromium.org/downloads)
- Update its path in build_driver() inside enrich_jobs_with_ai.py. and each spider
  
### Environment Variables
Create a .env file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### SQL Server Table
Create your table in SSMS:
```sql
CREATE TABLE JobListings (
   Id INT IDENTITY(1,1) PRIMARY KEY,
   Company NVARCHAR(255) NULL,
   JobTitle NVARCHAR(255) NULL,
   Location NVARCHAR(255) NULL,
   Link NVARCHAR(1000) NULL,
   Category NVARCHAR(100) NULL,
   Skills NVARCHAR(MAX) NULL,
   Years NVARCHAR(100) NULL,
   CitizenPR NVARCHAR(50) NULL
);
```

## How to run
Run a specific spider
```bash
scrapy crawl spider_name
```
Run all spiders
```bash
python run_all_spiders.py
```
Enrich latest raw file
```bash
python enrich_jobs_with_ai.py
```
Push to SQL Server
```bash
python push_to_SSMSSQL.py
```

### ⚠️ **Disclaimer**
- This project is for educational use only. 
- Always review and respect the robots.txt and terms of service of any website you scrape.
- AI output can be wrong, please verify on the original posting.
