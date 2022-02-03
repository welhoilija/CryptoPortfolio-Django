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
		price.objects.create(price=assetprice.get("last"), asset = asset)

