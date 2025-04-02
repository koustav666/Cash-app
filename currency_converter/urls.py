from django.urls import path
from .views import currency_conversion

urlpatterns = [
    path("conversion/<str:currency1>/<str:currency2>/<str:amount_of_currency1>/", currency_conversion, name="currency_conversion"),
]
