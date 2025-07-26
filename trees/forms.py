from django import forms

from accounts.models import Account
from trees.models import PlantedTree, Tree


class PlantTreeForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.none(), label="Conta")

    class Meta:
        model = PlantedTree
        fields = ['tree', 'age', 'latitude', 'longitude', 'account']
        widgets = {
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'age': forms.NumberInput(attrs={'min': 0}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = user.accounts.filter(  # type: ignore
            active=True)


class MultiPlantingForm(forms.Form):
    tree = forms.ModelChoiceField(
        queryset=Tree.objects.all(),
        label="Tree Type"
    )
    coordinates = forms.CharField(
        label="Coordinates (format: [(lat1, lon1), (lat2, lon2)])",
        widget=forms.Textarea(attrs={"rows": 5}),
        help_text="E.g., [(1.2123, 12.232), (15.1234, 12.444)]",
    )
