import sys

from icrawler.builtin import GoogleImageCrawler,BingImageCrawler

google_crawler = BingImageCrawler(storage={'root_dir': 'crawled6'})
google_crawler.crawl(keyword='Chave Seccionadora Rotativa', max_num=1000)