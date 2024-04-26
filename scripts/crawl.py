import sys

from icrawler.builtin import GoogleImageCrawler,BingImageCrawler

google_crawler = GoogleImageCrawler(storage={'root_dir': 'crawled5'})
google_crawler.crawl(keyword='válvula esfera', max_num=1000)