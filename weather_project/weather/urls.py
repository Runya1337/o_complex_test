from . import views
from django.urls import path
from .views import autocomplete_city

urlpatterns = [
    path('autocomplete/city/', autocomplete_city, name='autocomplete_city'),
    path('', views.index)
]
