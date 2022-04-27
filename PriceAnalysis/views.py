from django.shortcuts import render
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from .forms import *
from django.contrib import messages

# Create your views here.


def home(request):
    user = request.user
    assets = Asset.objects.all()
    holdings = Holding.objects.all()


    total_balance = 0

    holdings_by_value = {}
    for i in holdings:
        holdings_by_value[i.asset.desc] = i.amount * i.asset.price_set.all().last().last_price

    for i in holdings:
        total_balance += i.amount * i.asset.price_set.all().last().last_price


        # if this is a POST request we need to process the form data
    if request.method == 'POST':


        # create a form instance and populate it with data from the request:
        AddAssetform = AddAssetForm(request.POST, prefix="Add Asset")

        
        # check whether the form is valid:
        if AddAssetform.is_valid():
            if Asset.objects.filter(ticker=AddAssetform.cleaned_data['Asset_ticker']).exists():
                messages.warning(request, 'Asset already added')
            else:
                #Add asset to db
                Asset.objects.create(ticker=AddAssetform.cleaned_data["Asset_ticker"], desc=AddAssetform.cleaned_data['Asset_Description'])
                messages.success(request, "Asset added")
    else:
        AddAssetform = AddAssetForm(prefix="Add Asset")

    if request.method == 'POST' and not AddAssetform.is_valid():
        #If addassetform is not valid, then it must be the holdingform
        AddHoldingform = AddHoldingForm(request.POST, prefix="Add Holding")
        AddAssetform = AddAssetForm(prefix="Add Asset")
        if AddHoldingform.is_valid():
            amount = AddHoldingform.cleaned_data["Amount"]
            if amount < 0:
                raise Exception("cant add negative amount")

            #Add asset to db
            Holding.objects.update_or_create(asset=AddHoldingform.cleaned_data["Asset"], defaults={"amount":AddHoldingform.cleaned_data["Amount"]})
            messages.success(request, "Holding added or modified")


    else:

        AddHoldingform = AddHoldingForm(prefix="Add Holding")
    if len(holdings) > 0:
        largest_asset =  max(holdings_by_value, key=holdings_by_value.get)
    else:
        largest_asset = None

    context = {
    "largest_asset": largest_asset,
    "total_balance": round(total_balance),
    "assets": assets,
    "holdings": holdings,
    "AddAssetform": AddAssetform,
    "AddHoldingForm": AddHoldingform,
    }

    return render(request, "home.html", context)

def charttest(request):
    return render(request, "charttest.html")


def getdata(request):
    assets = Asset.objects.all()

    if request.accepts('XMLHttpRequest') and request.method =="GET":
        json = {}
        for asset in assets:
            json[asset.ticker] = asset.price_set.all().last().last_price
            json[asset.ticker + "change"] = asset.price_set.all().last().pricechange




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


def addHolding(request):


    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = AddHoldingForm(request.POST)

        
        # check whether the form is valid:
        if form.is_valid():
            amount = form.cleaned_data["Amount"]
            if amount < 0:
                raise Exception("cant add negative amount")

            #Add asset to db
            Holding.objects.update_or_create(asset=form.cleaned_data["Asset"], defaults={"amount":form.cleaned_data["Amount"]})
            messages.success(request, "Holding added or modified")



    else:

        form = AddHoldingForm()





    return render(request, 'addholding.html', {'form': form,})

