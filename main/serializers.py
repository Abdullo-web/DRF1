from rest_framework import serializers
from django.db.models import Avg
from .models import User, Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'text']


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True
    )
    owner_data = UserDataSerializer(source='owner', read_only=True)

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )
    category_data = CategoryDataSerializer(source='category', read_only=True)

    reviews = ReviewSerializer(many=True, read_only=True)
    review_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price',
            'category', 'category_data',
            'owner', 'owner_data', 'created_at',
            'avg_rating', 'review_count', 'reviews'
        ]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Название не может быть пустым.')
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Цена должна быть больше нуля.')
        return value

    def get_review_count(self, product):
        return product.reviews.count()

    def get_avg_rating(self, product):
        result = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if result is None:
            return None
        return round(result, 2)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avg_rating'] = self.get_avg_rating(instance)
        return data


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'rating', 'product']
        read_only_fields = ['id']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5.')
        return value

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв на этот товар.')

        return data