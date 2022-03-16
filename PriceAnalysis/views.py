from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from .forms import *
from django.contrib import messages

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



def addasset(request):


    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = AddAssetForm(request.POST)

        
        # check whether the form is valid:
        if form.is_valid():
        	if Asset.objects.filter(ticker=form.cleaned_data['Asset_ticker']).exists():
        		messages.warning(request, 'Asset already added')
        	else:
        		#Add asset to db
        		Asset.objects.create(ticker=form.cleaned_data["Asset_ticker"], desc=form.cleaned_data['Asset_Description'])
        		messages.success(request, "Asset added")



    else:

        form = AddAssetForm()





    return render(request, 'addasset.html', {'form': form,})
