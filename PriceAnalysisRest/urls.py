from django.urls import path
from PriceAnalysisRest.views import Auth

urlpatterns = [
	path("auth/", Auth.as_view(), name="web3_auth")
]