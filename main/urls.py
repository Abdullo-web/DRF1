from django.urls import path
from .views import products, product_detail, categories, product_reviews

urlpatterns = [
    path('products/', products),
    path('products/<int:pk>/', product_detail),
    path('products/<int:pk>/reviews/', product_reviews),
    path('categories/', categories),
]