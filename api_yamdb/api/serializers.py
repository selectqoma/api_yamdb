from rest_framework import serializers


class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.Serializer):
    class Meta:
        fields = ['username',
                  'email',
                  'bio',
                  'first_name',
                  'last_name',
                  'role'
                  ]
