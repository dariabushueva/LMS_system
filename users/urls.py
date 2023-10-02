from django.urls import path

from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('destroy/<int:pk>/', UserDestroyAPIView.as_view(), name='user_destroy'),
]
