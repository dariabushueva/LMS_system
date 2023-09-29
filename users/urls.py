from django.urls import path

from users.apps import UsersConfig
from .views import *

app_name = UsersConfig.name

urlpatterns = []
