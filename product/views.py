from django.shortcuts import render
from .serializers import ProductSerializers
from .models import Product
from rest_framework.decorators import APIView
# from rest_framework.generics import ListAPIView,CreateAPIView,DestroyAPIView,UpdateAPIView
from .serializers import ProductSerializers
from drf_spectacular.utils import extend_schema




# class PrListV(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
    

# class PrCreateV(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
    
# class PrDeleteeV(DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
    
# class PrUpdateV(UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
    
 
 
# from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

# class Prcrlis(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
    
# class Prcrlist(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializers
    
from rest_framework.viewsets import ModelViewSet

class Pro(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
   