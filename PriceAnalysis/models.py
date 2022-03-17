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

    

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.price, self.created_at)

class Holding(models.Model):

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    #some assets have a lot of decimals in the base units...
    amount = models.DecimalField(max_digits=65, decimal_places=19)



