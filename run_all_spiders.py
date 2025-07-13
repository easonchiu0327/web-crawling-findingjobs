from scrapy.crawler import CrawlerProcess
# import all your spider classes
from findingjobs.spiders import shifts7, accenture, agrius, charter, firsttecpro, horizon, ibits, opensail, projectline, pushinteractions, sasksoftware, testspider, univerus, vendasta, wbm
import os
from datetime import datetime
# Define your output directory and filename
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)  # create dir if not exist
# Get current time string (e.g., 2025-07-14_01-30-00)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
process = CrawlerProcess(settings={
    # The FEEDS setting tells Scrapy where and how to save the scraped data.
    "FEEDS": {
        os.path.join(output_dir, f"Result_{timestamp}.json"): {"format": "json"},
    },
})
# Add each spider to the process
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
process.crawl(testspider.TestSpider)
process.crawl(univerus.UniverusSpider)
process.crawl(vendasta.VendastaSpider)
process.crawl(wbm.WbmSpider)

process.start()

