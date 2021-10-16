from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.shortcuts import get_object_or_404

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
    slug = serializers.SlugField(
        max_length=50, required=True,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )
    name = serializers.CharField(max_length=256, required=True)

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50, required=True,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    name = serializers.CharField(max_length=256, required=True)

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category_read = CategorySerializer(read_only=True, source='category')
    genre_read = GenreSerializer(many=True, read_only=True, source='genre')
    rating = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=False)
    category = serializers.SlugField(write_only=True, required=True)
    genre = serializers.ListField(
        child=serializers.SlugField(max_length=50),
        write_only=True, required=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre_read',
            'category_read', 'category', 'genre')
        model = Title

    def create(self, validated_data):
        category_slug = validated_data.pop('category')
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)

        if category_slug is not None:
            category_obj = get_object_or_404(Category, slug=category_slug)
            title.category = category_obj
            title.save()

        if genres:
            for genre_slug in genres:
                genre_obj = Genre.objects.get(slug=genre_slug)
                title.genre.add(genre_obj)

        return title

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            category_slug = validated_data.pop('category')
            if category_slug is not None:
                category_obj = get_object_or_404(Category, slug=category_slug)
                instance.category = category_obj
        if 'genres' in validated_data:
            genres = validated_data.pop('genre')
            if genres:
                instance.genre.clear()
                for genre_slug in genres:
                    genre_obj = Genre.objects.get(slug=genre_slug)
                    instance.genre.add(genre_obj)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def to_representation(self, value):
        rep = super().to_representation(value)
        rep['category'] = rep['category_read']
        del rep['category_read']
        rep['genre'] = rep['genre_read']
        del rep['genre_read']
        return rep
