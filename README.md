# Saskatchewan IT Job AI-Scraper

This project is a web scraping bot combining Scrapy and Selenium, enhanced with OpenAI API for analyzing job descriptions.
It collects IT-related job listings from multiple websites, enriches them with **AI**, and saves results into a SQL Server database.

# Skills
- Spider: Python, OpenAI API, Scrapy, Selenium, XPath, Prompt, JSONL
- SQL:
- .Net Framwork:
- Azure:

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
## Deployment on Azure

## Why Azure?
- Free **$100/year student account** for development and testing  
- Smooth integration with **.NET framework & Visual Studio**  
- **Scalable tiers** for SQL Database (Basic DTU for cost control)  
- Built-in **firewall, authentication, and endpoint management**  
- Easy migration from **local SQL Server → Azure SQL**  

---

## Deployment Steps

### 1. Azure Setup
1. Choose **Azure for Students Subscription** ($100/year credit).  
2. Open **Cloud Shell** → create a **Storage Account**.  
3. Create **Resource Group**  
   - Naming convention: `{resourcetype}-{name}-{location}-{environment}-{instance}`  
   - Pin to dashboard for easy management.  

### 2. Web App Service
- Create **App Service** for hosting the ASP.NET website.  

### 3. Azure SQL Database
1. Create **SQL Database** + SQL Server.  
2. Use **SQL + Azure AD Authentication**.  
3. Set SQL login password.  
4. Scale to **Basic DTU (5 DTUs, 2GB max)** for cost savings.  
5. Configure **public endpoint** connectivity.  
6. Set firewall rules:  
   - Local SSMS ↔ Azure SQL (via IP whitelist)  
   - Azure Web App ↔ Azure SQL (internal Azure connectivity).  
7. If laptop IP changes → update firewall settings in SQL Server network configuration.  

### 4. Database Migration
- One-time transfer from **local SQL Server → Azure SQL**:  
   1. In SSMS → `Tasks → Export Data-tier Application` → save to Azure Storage (BACPAC).  
   2. Import BACPAC into Azure SQL.  
   3. Configure authentication & pricing tier (adjustable on demand).  

### 5. Connection String & Secrets
1. Update `web.config` to point to Azure SQL.  
2. Store secrets on Azure:  
   - Go to **Configuration → Environment Variables** → add `SQLDB_CONN`.  
3. Add helper class for calling:  
   ```csharp
   Environment.GetEnvironmentVariable("SQLDB_CONN")

4. Adjust DAO connection functions to use env var.

### 6. Deploy ASP.NET to Azure  

1. In Visual Studio:
   - Right-click solution → **Publish** → Azure → App Service  
   - Sign in → select resource group → select App Service → publish  


### 7. Cost Optimization  

1. - **Basic DTU Tier** → optimized (~CA$0.20 daily).  
2. - Used **Azure Cost Analysis + Anomaly Insights** to track and reduce expenses.  


### 8. Future Improvements  

1. - Containerize spiders with **Azure Container Apps**.  


## Summary  

- On **Azure App Service** → app uses `SQLDB_CONN` env variable.  
- On **Local Dev** → connect via SSMS, but only when laptop SQL Server is running.  


## References  

- [Azure CLI Documentation (Microsoft Learn)](https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)  
- [YouTube: Azure SQL Database Tutorial (Part 1)](https://www.youtube.com/watch?v=EzdqO6jX8u4&list=PLdo4fOcmZ0oVSBX3Lde8owu6dSgZLIXfu&index=2)  
- [YouTube: Azure App Service + SQL Database Integration](https://www.youtube.com/watch?v=sW1OGB5ztZI&list=PLdo4fOcmZ0oVSBX3Lde8owu6dSgZLIXfu&index=2)

### ⚠️ **Disclaimer**
- This project is for educational use only. 
- Always review and respect the robots.txt and terms of service of any website you scrape.
- AI output can be wrong, please verify on the original posting.
