import sys

from icrawler.builtin import GoogleImageCrawler,BingImageCrawler

google_crawler = GoogleImageCrawler(storage={'root_dir': 'crawled8'})
google_crawler.crawl(keyword='valvula borboleta', max_num=1000)