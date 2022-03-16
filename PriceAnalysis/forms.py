from django import forms



class AddAssetForm(forms.Form):
    Asset_ticker = forms.CharField(label="Asset ticker using binance syntax", max_length=10)
    Asset_Description = forms.CharField(label="Asset Description", max_length=150)

    def __init__(self, *args, **kwargs):

        super(AddAssetForm, self).__init__(*args, **kwargs)
        self.fields["Asset_ticker"].widget.attrs.update({'class': 'form-control form-control-user', 'title': 'Asset in binance syntax'})
        self.fields["Asset_Description"].widget.attrs.update({'class': 'form-control form-control-user', 'title': 'Asset description'})

