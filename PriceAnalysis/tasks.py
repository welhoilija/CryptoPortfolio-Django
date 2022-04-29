#tasks.py

import ccxt
import random
import datetime
from PriceAnalysis.models import price, Asset

from celery import shared_task



@shared_task
def fetch_coin_price():
	binance = ccxt.binance({"verbose": True})

	for asset in Asset.objects.all():
		assetprice = binance.fetch_ticker(asset.ticker)
		pricechange = assetprice.get("percentage")
		print(assetprice)
		price.objects.create(
			last_price=assetprice.get("last"),
			pricechange=pricechange,
		  	asset = asset,
			)

"""{'symbol': 'BNB/USDT',
 'timestamp': 1648205620298,
  'datetime': '2022-03-25T10:53:40.298Z',
   'high': 416.6, 'low': 405.0, 'bid': 414.9,
    'bidVolume': 191.724,
     'ask': 415.0, 'askVolume': 365.5,
      'vwap': 412.59700037, 'open': 410.3,
       'close': 415.0, 'last': 415.0,
        'previousClose': '410.30000000',
         'change': 4.7, 'percentage': 1.146,
          'average': 412.65, 'baseVolume': 555348.894,
           'quoteVolume': 229135287.8226,"""


