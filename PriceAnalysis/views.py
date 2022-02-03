from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# Create your views here.


def home(request):
	assets = Asset.objects.all()


	context = {
	"assets": assets,
	}

	return render(request, "home.html", context)

def charttest(request):
	return render(request, "charttest.html")


def getdata(request):
	assets = Asset.objects.all()

	if request.accepts('XMLHttpRequest') and request.method =="GET":
		json = {}
		for asset in assets:
			json[asset.ticker] = asset.price_set.all().last().price


		data = json


		return  JsonResponse(data)


def assetview(request, asset_id):

	asset = Asset.objects.get(id=asset_id)


	context = {
	"asset": asset,
	}


	return render(request, "asset.html", context)