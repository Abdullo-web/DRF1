from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Review, Category
from .serializers import ProductSerializer, ReviewSerializer, ReviewCreateSerializer, CategorySerializer
from .pagination import CustomPagination


@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        product_list = Product.objects.all()

        category = request.query_params.get('category')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search = request.query_params.get('search')

        if category:
            product_list = product_list.filter(category_id=category)

        if min_price:
            product_list = product_list.filter(price__gte=min_price)

        if max_price:
            product_list = product_list.filter(price__lte=max_price)

        if search:
            product_list = product_list.filter(title__icontains=search)

        paginator = CustomPagination()
        page = paginator.paginate_queryset(product_list, request)
        serializer = ProductSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    if not request.user.is_authenticated:
        return Response({'error': 'Сначала войдите в аккаунт'}, status=401)

    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Товар не найден'}, status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=200)

    if not request.user.is_authenticated:
        return Response({'error': 'Сначала войдите в аккаунт'}, status=401)

    if product.owner != request.user:
        return Response({'error': 'Это не ваш товар'}, status=403)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=204)


@api_view(['GET', 'POST'])
def categories(request):
    if request.method == 'GET':
        category_list = Category.objects.all()
        serializer = CategorySerializer(category_list, many=True)
        return Response(serializer.data, status=200)

    if not request.user.is_authenticated:
        return Response({'error': 'Сначала войдите в аккаунт'}, status=401)

    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['GET', 'POST'])
def product_reviews(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Товар не найден'}, status=404)

    if request.method == 'GET':
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)

    if not request.user.is_authenticated:
        return Response({'error': 'Сначала войдите в аккаунт'}, status=401)

    serializer = ReviewCreateSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        serializer.save(user=request.user, product=product)
        result = ReviewSerializer(serializer.instance)
        return Response(result.data, status=201)

    return Response(serializer.errors, status=400)