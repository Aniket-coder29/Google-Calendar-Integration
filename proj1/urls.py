from django.contrib import admin
from django.urls import path,include

from authentication.views import CallbackView, RedirectOauthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('google_oauth/redirect/', RedirectOauthView),
    path('google_oauth/callback/', CallbackView)
]
