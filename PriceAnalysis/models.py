from django.db import models
from datetime import timedelta
from django.utils import timezone
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

    last_price = models.DecimalField(decimal_places=2, max_digits=12)

    pricechange = models.DecimalField(decimal_places=5, max_digits=8, default=None, null = True)

    

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.price, self.created_at)

class Holding(models.Model):


    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    #some assets have a lot of decimals in the base units...
    amount = models.DecimalField(max_digits=65, decimal_places=19)



    def __str__(self):
        return "%s %s" % (self.asset, self.amount)


    def calculate_PL(self, days):
        amount = self.amount
        asset = self.asset
        week_ago_date = timezone.now().date() - timedelta(days=days)

        price_before = price.objects.filter(created_at=week_ago_date).first()
        price_now = price.objects.latest("created_at")
        if price_before:
            return price_now.last_price - price_before.last_price
        else:
            return None
        pass


class contactdata(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True, null=True, max_length=2000)
    sender_mail = models.CharField(max_length=64)

    def __str__(self):
        return "%s %s" % (self.message, self.sender_mail)


