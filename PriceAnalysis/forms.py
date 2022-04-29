from django import forms
from .models import Asset, contactdata
import ccxt
from ccxt.base.errors import BadSymbol



class AddAssetForm(forms.Form):
    Asset_ticker = forms.CharField(label="Asset ticker using binance syntax", max_length=10)
    Asset_Description = forms.CharField(label="Asset Description", max_length=150)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddAssetForm, self).__init__(*args, **kwargs)
        self.fields["Asset_ticker"].widget.attrs.update({'class': 'form-control form-control-user', 'title': 'Asset in binance syntax'})
        self.fields["Asset_Description"].widget.attrs.update({'class': 'form-control form-control-user', 'title': 'Asset description'})

    def clean_Asset_ticker(self):
        ticker = self.cleaned_data["Asset_ticker"]
        binance = ccxt.binance({"verbose": True})
        try:
            ticker_info = binance.fetch_ticker(ticker)
        except BadSymbol:
            raise
        return ticker


class AddHoldingForm(forms.Form):
    Asset = forms.ModelChoiceField(queryset=Asset.objects.all())
    Amount = forms.DecimalField(max_digits=65, decimal_places=19)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AddHoldingForm, self).__init__(*args, **kwargs)
        self.fields["Asset"].widget.attrs.update({"class": "btn btn-secondary dropdown-toggle m-2 w-100", "type": "button", "id": "dropdownMenuButton1", "title": "Choose asset", "data-bs-toggle":"dropdown", "aria-expanded":"false"})
        self.fields["Amount"].widget.attrs.update({'class': 'form-control form-control-user m-2', 'title': 'Choose amount'})



class ContactForm(forms.ModelForm):
    class Meta:
        model = contactdata
        fields = ['message', 'sender_mail']
        labels = {
        "message": "Message",
        "sender_mail": "Email",
    }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["message"].widget.attrs.update({'class': 'form-control form-control-lg m-2', 'title': 'Choose amount'})
        self.fields["sender_mail"].widget.attrs.update({'class': 'form-control form-control-lg m-2', 'title': 'Choose amount'})

