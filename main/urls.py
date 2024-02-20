from django.urls import path
from .views import ImageConvertAPIView

urlpatterns = [
    path('convert', ImageConvertAPIView.as_view(), name='convert'),
]
