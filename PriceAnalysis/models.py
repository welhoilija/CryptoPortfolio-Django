from django.db import models

# Create your models here.


DEFAULT_ASSETS = (
    (1, 'BTC', 'sats', ''),
    (2, 'ETH', 'wei', ''),
)

class Asset(models.Model):
    #BINANCE TICKER
    ticker = models.CharField(max_length=5)

    desc = models.CharField(max_length=100)

    def __str__(self):
        return "%s %s" % (self.ticker, self.desc)

    class Meta:
        pass
        
#prices with timestaps for fancy graphs
class price(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    price = models.DecimalField(decimal_places=2, max_digits=12)

    
    """symbol":"DOTUSDT","priceChange":"-2.30000000"
    "priceChangePercent":"
    -11.214","weightedAvgPrice"
    :"19.01254871","prevClosePrice"
    :"20.52000000",
    "lastPrice":"18.21000000",
    "lastQty":"108.18000000",
    "bidPrice":"18.20000000",
    "bidQty":"839.73000000",
    "askPrice":"18.21000000",
    "askQty":"3594.75000000",
    "openPrice":"20.51000000",
    "highPrice":"20.55000000",
    "lowPrice":"18.03000000",
    "volume":"9203389.62000000",
    "quoteVolume":"174979893.41170000",
    "openTime":1643804041889,
    "closeTime":1643890441889,
    "firstId":264821465,
    "lastId":265135025,
    "count":313561
    """

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.price, self.created_at)

