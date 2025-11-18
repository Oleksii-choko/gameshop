from django import forms
from .models import Category,Platform,Genre, ContactMessage


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
        # Інпути ціни
        for name in ("price_min", "price_max"):
            self.fields[name].widget.attrs.update({
                "class": "form-control",
                "placeholder": "0",
                "inputmode": "decimal",
            })


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label='Імʼя')
    last_name = forms.CharField(max_length=50, label='Прізвище')
    email = forms.EmailField(label='Пошта')
    subject = forms.CharField(max_length=100, label='Тема')
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Ваше повідомлення...'}
        ),
        label='Повідомлення',
    )

    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']
