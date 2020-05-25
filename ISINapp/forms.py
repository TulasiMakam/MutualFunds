from django import forms
from ISINapp.models import MutualFunds

class MutualFundsForm(forms.ModelForm):
    class Meta():
        model = MutualFunds
        fields = ('ISIN',)