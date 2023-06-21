from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from .views import homepage
from django.conf.urls.static import static

urlpatterns = [
    path("", homepage, name="homepage"),
    
]
