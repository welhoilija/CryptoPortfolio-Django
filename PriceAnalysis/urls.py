from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('getdata', views.getdata, name='getdata'),
	path("chart", views.charttest, name="charttest"),
	path("asset/<str:asset_id>", views.assetview, name="assetview"),
	path("addasset", views.addasset, name="addassetview"),
	path("addHolding", views.addHolding, name="addHoldingview"),
	path("login", views.login, name="loginview"),

]