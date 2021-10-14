from .serializers import (
    SendCodeSerializer, LogInSerializer, UserSerializer, AdminUserSerializer
)
from users.models import User
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from django.core.mail import send_mail
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
import uuid
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdmin, IsModerator, IsAuthor, \
    IsAuthenticatedOrReadOnly
from .serializers import ReviewSerializer, CommentSerializer

from titles.models import Title, Review


@api_view(['POST'])
def send_code(request):
    serializer = SendCodeSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    confirmation_code = str(uuid.uuid4())
    if serializer.is_valid():

        if User.objects.filter(email=email, username=username).exists():
            user = User.objects.get(email=email, username=username)
            user.confirmation_code = confirmation_code
        else:
            if User.objects.filter(
                    email=email
            ).exists() or User.objects.filter(username=username).exists():
                return Response(
                    {'error': 'Такой пользователь уже существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            User.objects.create_user(email=email, username=username)
        mail_subject = 'API_Yamdb: Ваш код для авторизации'
        mail_message = f'Скопируйте код: {confirmation_code}'
        send_mail(mail_subject, mail_message, 'API_Yamdb <admin@yamdb.ru>',
                  (email,))
        return Response(
            request.data,
            status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_token(request):
    serializer = LogInSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if confirmation_code == str(user.confirmation_code):
            token = RefreshToken.for_user(user)
            return Response({f'Ваш токен: {token.access_token}'},
                            status=status.HTTP_200_OK)
        return Response('Неправильный код',
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    filter_fields = ('role',)
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


class UserInfo(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response('Вы не авторизированы',
                        status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=request.user.username)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response('Вы не авторизированы',
                        status=status.HTTP_401_UNAUTHORIZED)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthor | IsModerator | IsAdmin
    ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        author = self.request.user
        serializer.save(
            author=author,
            title=title

        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthor | IsModerator | IsAdmin
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )