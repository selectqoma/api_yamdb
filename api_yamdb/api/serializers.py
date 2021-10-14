from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User
from titles.models import Review, Comment


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
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            'id', 'title', 'author', 'text', 'score', 'pub_date')
        read_only_fields = ('title', 'author', 'pub_date')

    def validate(self, attrs):
        review_obj_exists = Review.objects.filter(
            author=self.context.get('request').user,
            title=self.context.get('view').kwargs.get('title_id')
        ).exists()
        if review_obj_exists and self.context.get('request').method == 'POST':
            raise serializers.ValidationError('Вы уже оставляли отзыв')
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'id', 'review', 'author', 'text', 'pub_date'
        )
        read_only_fields = ('review', 'author', 'pub_date')
