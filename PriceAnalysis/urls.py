from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('getdata', views.getdata, name='getdata'),
	path("chart", views.charttest, name="charttest"),
	path("<str:asset_id>", views.assetview, name="assetview"),

]