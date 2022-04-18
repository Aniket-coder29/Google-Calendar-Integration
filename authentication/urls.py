from . import views
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', views.home, name='home'),
    path('google_oauth/redirect/', views.RedirectOauthView,name='RedirectOauthView'),
    path('google_oauth/callback/', views.CallbackView,name='CallbackView')

]
