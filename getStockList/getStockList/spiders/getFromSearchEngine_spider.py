# -*- coding: utf-8 -*-

import scrapy
import urllib

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.contrib.closespider import CloseSpider

from pymongo import MongoClient
from selenium import webdriver
import time
import re

from getStockList.items import GetStockListItem

class getStockListSpider(CrawlSpider):
    
    print " >>>>> >>>>> >>>> stockInfo crawler start"

    def __init__(self, *args, **kwargs):
        self.curUrl = 'http://m.stock.naver.com/sise/siseGroupDetail.nhn?menu=upjong&no=154#siseMenuList'
        self.error_code = 0;
        self.parameter = kwargs.get('p_args')
        print ">>>>> url: ", self.curUrl
        self.driver = webdriver.Firefox(executable_path=r'C:\Users\developer\geckodriver.exe')
        self.start_urls = [self.curUrl]
        super(getStockListSpider, self).__init__(*args, **kwargs)
 
    name = 'getStockList'
 
    def parse(self, response):
 
        print ">>>>> parse start"
        
        if(self.error_code == 1):
            print ">>>>> error:", 'one of mandatory arguments is not retrieved'
            raise CloseSpider()
        
        self.driver.get(response.url)
        
        def frange(start, stop, step):
            i = start
            while i < stop:
                yield i
                i += step
        
        for i in frange(0.5, 1.0, 0.1):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        
        hxs = Selector(text=self.driver.find_element_by_class_name('_list_wrap').get_attribute('innerHTML'))
        iteratedObjectLiXPath = '//tr'
        objects = hxs.xpath(iteratedObjectLiXPath)
        curNo = 0
        
        for o in objects:
            if(o.xpath('td/span/text()')[0].extract() == '*'):
                stockItem = o.xpath('td/span/text()')[1].extract()
                stockPrice = o.xpath('td/span/text()')[2].extract()
            else:
                stockItem = o.xpath('td/span/text()')[0].extract()
                stockPrice = o.xpath('td/span/text()')[1].extract()
                
            s = str(o.xpath('@onclick').extract()[0])
            s = s.split(";")[1]
            
            stockNo = s[s.find("(") + 1:s.find(")")]
            stockNo = stockNo.replace("'", "")
            
            print " >>>>> #", (curNo + 1), ", stockItem: ", stockItem, ", stockPrice:", stockPrice, ", stockNo: ", stockNo
            curNo = curNo + 1
            
        self.driver.close()
