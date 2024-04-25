import sys

from icrawler.builtin import BingImageCrawler

google_crawler = BingImageCrawler(storage={'root_dir': 'crawled6'})
google_crawler.crawl(keyword='circuitbreak', max_num=1000)