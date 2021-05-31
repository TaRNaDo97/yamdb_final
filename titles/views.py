from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import EMAIL

from .filters import TitlesFilter
from .models import Category, Genre, Title, User
from .permissions import AuthorPermission, IsAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          EmailRegistrationSerializer, GenreSerializer,
                          NewTokenObtainSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserMeSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH'],
            serializer_class=UserMeSerializer,
            permission_classes=[IsAuthenticated], url_path='me')
    def me(self, request):
        serializer = UserMeSerializer(
            self.request.user, data=request.data, partial=True)
        if serializer.is_valid():
            if self.request.method == 'PATCH':
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class EmailRegistrationView(APIView):
    serializer_class = EmailRegistrationSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User(
            username=email,
            email=email,
        )
        password = User.objects.make_random_password()
        conformation_code = User.objects.make_random_password()
        user.set_password(password)
        serializer.save(
            username=user.username,
            password=user.password,
            conformation_code=conformation_code
        )
        status_code = status.HTTP_201_CREATED
        response = {
            'statusCode': status_code,
            'message': 'Код доступа выслан на вашу электронную почту',
        }

        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения - {password}',
            EMAIL,
            [email],
            fail_silently=False
        )

        return Response(response, status=status_code)


class GetTokenView(APIView):
    serializer_class = NewTokenObtainSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        conformation_code = serializer.validated_data['conformation_code']
        user = User(
            email=email,
            conformation_code=conformation_code,
        )
        refresh = RefreshToken.for_user(user)

        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response)


class MyMixinsSet(GenericViewSet, mixins.ListModelMixin,
                  mixins.CreateModelMixin, mixins.DestroyModelMixin):

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [SearchFilter]
    search_fields = ['name', ]


class CategoryViewSet(MyMixinsSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(MyMixinsSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return TitleWriteSerializer
        return TitleReadSerializer

    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter


class RewievViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorPermission]

    def get_queryset(self):
        """Функция для получения отзывов"""
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(
            title=title,
            author=self.request.user
        )


class CommentViewSet(ModelViewSet):
    """Вьюсет для доступа к модели Comment"""
    serializer_class = CommentSerializer
    permission_classes = [AuthorPermission]

    def get_queryset(self):
        """Функция для получения комментариев"""
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        review = get_object_or_404(
            title.reviews.all(),
            pk=self.kwargs['review_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        review = get_object_or_404(
            title.reviews.all(),
            pk=self.kwargs['review_id']
        )
        serializer.save(
            review=review,
            author=self.request.user
        )
