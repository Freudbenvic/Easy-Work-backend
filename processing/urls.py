from django.urls import path
from .views import BackgroundRemovalView, HistoriqueView

urlpatterns = [
    path('background-removal/', BackgroundRemovalView.as_view(), name='background-removal'),
    path('historique/', HistoriqueView.as_view(), name='historique'),
]
