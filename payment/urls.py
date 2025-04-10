from payment import views
from django.urls import path


urlpatterns = [
    path('pay_to_user/', views.pay_to_user, name='pay_to_user'),
    path('check_transaction/', views.check_transactions, name='check_transaction'),
    path('request_payment/', views.request_payment, name='request_payment'),
    path('promote/', views.promote_to_admin, name='promote'),
]
