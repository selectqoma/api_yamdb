from rest_framework import serializers
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
