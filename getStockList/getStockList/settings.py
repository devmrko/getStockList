# -*- coding: utf-8 -*-

BOT_NAME 			= 'getStockList'
SPIDER_MODULES 		= ['getStockList.spiders']
NEWSPIDER_MODULE 	= 'getStockList.spiders'
ITEM_PIPELINES 		= {'getStockList.pipelines.MongoDBPipeline': 1000, }

DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
	'getStockList.rotate_useragent.RotateUserAgentMiddleware' :400
}

# put your mongoDB's account info
MONGODB_SERVER	= "etc-dbs"
MONGODB_PORT = 27017
MONGODB_DB 	= "memo"
MONGODB_COLLECTION 	= "stockInfo"
DOWNLOAD_DELAY = 30
CONCURRENT_REQUESTS = 1