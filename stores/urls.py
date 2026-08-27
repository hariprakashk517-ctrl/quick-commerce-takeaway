from django.urls import path
from .views import *

urlpatterns = [
    path('all/', StoreListCreateAPIView.as_view(), name="store-list-create"),
    path('<int:pk>/', StoreDetailAPIView.as_view(), name="store-detail"),
]
