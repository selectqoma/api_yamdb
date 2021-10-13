from .serializers import SendCodeSerializer
from rest_framework.views import APIView
from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status
import uuid


@api_view(['POST'])
def send_code(request):
    serializer = SendCodeSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    confirmation_code = uuid.uuid4()
    if serializer.is_valid():
        user = User.objects.filter(email=email).exists()
        if not user:
            User.objects.create_user(email=email, username=username)
        User.objects.filter(username=username).update(
            confirmation_code=confirmation_code
        )
        mail_subject = 'API_Yamdb: Ваш код для авторизации'
        mail_message = f'Скопируйте код: {confirmation_code}'
        send_mail(mail_subject, mail_message, 'API_Yamdb <admin@yamdb.ru>', email)
        return Response(
            f'Проверьте вашу почту, код был отправлен на {email}',
            status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
