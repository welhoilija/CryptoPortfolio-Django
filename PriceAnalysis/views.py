from django.shortcuts import render
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.
from django.views.decorators.http import require_http_methods
from django.conf import settings

from web3auth.forms import SignupForm

def home(request):
    user = request.user
    assets = Asset.objects.all()
    if not user.is_anonymous:
        holdings = user.holdings.all()
    else:
        holdings = []


    total_balance = 0

    holdings_by_value = {}
    for i in holdings:
        holdings_by_value[i.asset.desc] = i.amount * i.asset.price_set.all().last().last_price

    for i in holdings:
        total_balance += i.amount * i.asset.price_set.all().last().last_price


        # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        AddAssetform = AddAssetForm(user, request.POST, prefix="Add Asset")

        # check whether the form is valid:
        if AddAssetform.is_valid():

            if Asset.objects.filter(ticker=AddAssetform.cleaned_data['Asset_ticker']).exists():
                messages.warning(request, 'Asset already added')

            else:
                #Add asset to db
                Asset.objects.create(ticker=AddAssetform.cleaned_data["Asset_ticker"], desc=AddAssetform.cleaned_data['Asset_Description'])
                messages.success(request, "Asset added")

    else:
        AddAssetform = AddAssetForm(user, prefix="Add Asset")

    if request.method == 'POST' and not AddAssetform.is_valid():
        #If addassetform is not valid, then it must be the holdingform
        AddHoldingform = AddHoldingForm(user, request.POST, prefix="Add Holding")
        AddAssetform = AddAssetForm(user ,prefix="Add Asset")
        if AddHoldingform.is_valid():
            amount = AddHoldingform.cleaned_data["Amount"]
            if amount < 0:
                raise Exception("cant add negative amount")

            #Add asset to db
            holding = Holding.objects.update_or_create(asset=AddHoldingform.cleaned_data["Asset"], defaults={"amount":AddHoldingform.cleaned_data["Amount"]})
            messages.success(request, "Holding added or modified")
            user.holdings.add(holding[0])
            user.save()


    else:

        AddHoldingform = AddHoldingForm(user ,prefix="Add Holding")
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
    "user": user,
    }

    return render(request, "portfolio.html", context)




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
@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        pass

    context = {}
    return render(request, 'login.html', context)



def frontpage(request):

    context = {
        "user": request.user,
    }
    return render(request, 'frontpage.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
    
def loading_view(request):
    return render(request, "loading.html")
    pass


def contactview(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Form uploaded successfully")

    form = ContactForm()
    context= {
    "form": form
    }
    return render(request, "contact.html", context)




@require_http_methods(["GET", "POST"])
def signup_view(request):
    """
    1. Creates an instance of a SignupForm.
    2. If the registration is closed or form has errors, returns form with errors
    3. If the form is valid, saves the user without saving to DB
    4. Sets the user address from the form, saves it to DB
    5. Logins the user using web3auth.backend.Web3Backend
    6. Redirects the user to LOGIN_REDIRECT_URL or 'next' in get or post params
    :param request: Django request
    :param template_name: Template to render
    :return: rendered template with form
    """
    form = SignupForm()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            addr_field = app_settings.WEB3AUTH_USER_ADDRESS_FIELD
            setattr(user, addr_field, form.cleaned_data[addr_field])
            user.save()
            login(request, user, 'web3auth.backend.Web3Backend')
            return redirect(get_redirect_url(request))
    return render(request, 'signup.html', {'form': form})