from rest_framework import serializers

from titles.models import Category, Genre, Title
from users.models import User


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Неверное имя пользователя')
        return value


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username",
                  "bio", "email", "role")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'bio',
                  'first_name',
                  'last_name',
                  'role'
                  ]
        read_only_fields = ('role', )


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(max_length=50, required=True)
    name = serializers.CharField(max_length=256, required=True)

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(max_length=50, required=True)
    name = serializers.CharField(max_length=256, required=True)

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.IntegerField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category')
        model = Title

    def create(self, validated_data):
        category_slug = validated_data.pop('category')
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        if category_slug is not None:
            category_obj = Category.objects.get(slug=category_slug)
            title.category = category_obj

        if genres:
            for genre_slug in genres:
                genre_obj = Genre.objects.get(slug=genre_slug)
                title.genre.add(genre_obj)

        return title
