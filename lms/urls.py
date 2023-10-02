from django.urls import path

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter

from lms.views import *

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_destroy'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
] + router.urls

