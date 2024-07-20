from .models import City
from django.forms import ModelForm, TextInput


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'id': 'cityInput',  # Указываем ID для использования в JavaScript
                'placeholder': 'Введите город',
                'autocomplete': 'off'  # Отключаем автозаполнение браузера
            })
        }
        