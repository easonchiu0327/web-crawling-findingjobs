from scrapy.crawler import CrawlerProcess
# import all your spider classes
from findingjobs.spiders import shifts7, accenture, agrius, charter, firsttecpro, horizon, ibits, opensail, projectline, pushinteractions, sasksoftware, univerus, vendasta, wbm
from push_to_SSMSSQL import push_json_to_ssms
import os
from datetime import datetime

def run_spiders():
    # === Scrapy Configuration ===
    # Define your output directory and filename
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # create dir if not exist
    # Get current time string (e.g., 2025-07-14_01-30-00)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    process = CrawlerProcess(settings={
        # The FEEDS setting tells Scrapy where and how to save the scraped data.
        "FEEDS": {
            os.path.join(output_dir, f"Result_{timestamp}.jsonl"): {"format": "jsonlines"},
            os.path.join(output_dir, f"Result_{timestamp}.csv"): {"format": "csv"},
        },
    })

    # Add each spider to the process
    # 14 spiders for now 2025/08/12
    process.crawl(shifts7.A7shiftsSpider)
    process.crawl(accenture.AccentureSpider)
    process.crawl(agrius.AgriusSpider)
    process.crawl(charter.CharterSpider)
    process.crawl(firsttecpro.FirsttecproSpider)
    process.crawl(horizon.HorizonSpider)
    process.crawl(ibits.IbitsSpider)
    process.crawl(opensail.OpensailSpider)
    process.crawl(projectline.ProjectlineSpider)
    process.crawl(pushinteractions.PushinteractionsSpider)
    process.crawl(sasksoftware.SasksoftwareSpider)
    process.crawl(univerus.UniverusSpider)
    process.crawl(vendasta.VendastaSpider)
    process.crawl(wbm.WbmSpider)

    # === Run the spiders ===
    process.start()

    # === Insert into SQL Server ===
    push_json_to_ssms()

if __name__ == "__main__":
    run_spiders()
