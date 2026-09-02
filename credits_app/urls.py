from django.urls import path
from .views import MyCreditView

urlpatterns = [
    path('me/', MyCreditView.as_view(), name='my-credit'),
]
