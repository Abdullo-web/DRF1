from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products/',Pro)
urlpatterns = router.urls

# urlpatterns = [
#     path('product/',Prcrlis.as_view()),
#     path('product/<int:pk>/',Prcrlist.as_view()),
#     # path('products_create/',PrCreateV.as_view()),
#     # path('products_delete/<int:pk>/delete',PrDeleteeV.as_view()),
#     # path('products_update/<int:pk>/update',PrUpdateV.as_view()),
# ]