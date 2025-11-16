from django import forms
from .models import Category,Platform,Genre


class GameFilterForm(forms.Form):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        to_field_name='slug',
    )
    platform = forms.ModelMultipleChoiceField(
        queryset=Platform.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    genre = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    price_min = forms.DecimalField(required=False,min_value=0)
    price_max = forms.DecimalField(required=False,min_value=0)

    require_all_platforms = forms.BooleanField(required=False)
    require_all_genres = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # приклад для інпутів ціни
        for name in ('price_min', 'price_max'):
            self.fields[name].widget.attrs.update({'class': 'form-control', 'placeholder': '0'})