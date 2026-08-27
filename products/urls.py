from django.urls import path
from .views import *

urlpatterns = [
    path('all/', ProductListCreateAPIView.as_view()),
    path('<int:pk>/', ProductDetailAPIView.as_view()),
]
