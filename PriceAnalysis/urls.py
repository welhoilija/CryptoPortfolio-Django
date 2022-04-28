from django.urls import path
from . import views

urlpatterns = [
	path("", views.frontpage, name="Frontpage"),
	path('portfolio', views.home, name='portfolio'),
	path('getdata', views.getdata, name='getdata'),
	path("chart", views.charttest, name="charttest"),
	path("asset/<int:asset_id>", views.assetview, name="assetview"),
	path("addasset", views.addasset, name="addassetview"),
	path("addHolding", views.addHolding, name="addHoldingview"),
	path("login", views.login, name="loginview"),
	path("logout", views.logout_view, name="logoutview"),

]