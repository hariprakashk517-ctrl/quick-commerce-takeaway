from django.urls import path
from .views import *

urlpatterns = [
    path('all/', InventoryListCreateAPIView.as_view()),
    path('<int:pk>/', InventoryDetailAPIView.as_view()),
]
