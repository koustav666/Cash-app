from payment import views
from django.urls import path


urlpatterns = [
    path('pay_to_user/', views.pay_to_user, name='pay_to_user'),
    path('check_transaction/', views.check_transactions, name='check_transaction'),
]
