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
# ⚠️ Disclaimer
This project is for educational use only. 
Always review and respect the robots.txt and terms of service of any website you scrape.

⚠️ **Note:** This project attempts to collect IT-related job postings, but due to inconsistencies on job boards, some non-IT roles may appear in the results. I will figure it out and slove this issue in the furure.
