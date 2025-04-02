from django.urls import path
from register import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login_view"), 
    path('logout/', views.logout_view, name='logout_view'), 
]
