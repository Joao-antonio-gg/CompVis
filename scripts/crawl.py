import sys

from icrawler.builtin import GoogleImageCrawler,BingImageCrawler

google_crawler = BingImageCrawler(storage={'root_dir': 'crawled6'})
google_crawler.crawl(keyword='chave comutadora', max_num=1000)