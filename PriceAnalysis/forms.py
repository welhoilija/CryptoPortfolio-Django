from django import forms
from .models import Asset



class AddAssetForm(forms.Form):
    Asset_ticker = forms.CharField(label="Asset ticker using binance syntax", max_length=10)
    Asset_Description = forms.CharField(label="Asset Description", max_length=150)

    def __init__(self, *args, **kwargs):

        super(AddAssetForm, self).__init__(*args, **kwargs)
        self.fields["Asset_ticker"].widget.attrs.update({'class': 'form-control form-control-user', 'title': 'Asset in binance syntax'})
        self.fields["Asset_Description"].widget.attrs.update({'class': 'form-control form-control-user', 'title': 'Asset description'})


class AddHoldingForm(forms.Form):
    Asset = forms.ModelChoiceField(queryset=Asset.objects.all())
    Amount = forms.DecimalField(max_digits=65, decimal_places=19)

    def __init__(self, *args, **kwargs):

        super(AddHoldingForm, self).__init__(*args, **kwargs)
        self.fields["Asset"].widget.attrs.update({"class": "btn btn-secondary dropdown-toggle m-2 w-100", "type": "button", "id": "dropdownMenuButton1", "title": "Choose asset", "data-bs-toggle":"dropdown", "aria-expanded":"false"})
        self.fields["Amount"].widget.attrs.update({'class': 'form-control form-control-user m-2', 'title': 'Choose amount'})