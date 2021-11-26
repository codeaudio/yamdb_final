import uuid

from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.custom_mixins import CustomMixin
from api.models import Category, Genre, Title
from api.permissions import (RoleCategory, RoleGenreOrTitle,
                             RoleReviewOrComment, RoleUser)
from api.serializers import (CategorySerializer, CommentSerializerGet,
                             CommentSerializerPost, CustomSerializer,
                             EmailSerializer, GenreSerializer,
                             ReviewSerializerGet, ReviewSerializerPost,
                             TitleSerializerGet, TitleSerializerPost,
                             UserSerializer)
from api.service import send_email

from .expressions import Round
from .filters import TitleFilter
from .models import Review

CustomUser = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [RoleUser]
    lookup_field = 'username'
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['pub_date', 'username', ]

    def get_object(self):
        me = self.kwargs.get('username')
        if me == 'me':
            return self.request.user
        return super().get_object()


class EmailViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        get_object_or_404(CustomUser, email=email)
        code = uuid.uuid4().hex
        user = CustomUser.objects.filter(email=email)
        user.update(confirmation_code=code)
        send_email(email=email, confirmation_code=str(code))
        return Response(status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [RoleReviewOrComment]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializerGet
        return CommentSerializerPost

    def perform_create(self, serializer):
        review_id = get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review_id
        )

    def get_queryset(self):
        get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id')
        )
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [RoleReviewOrComment]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        if title_id is not None:
            title = get_object_or_404(
                Title, id=self.kwargs.get('title_id')
            )
            return title.reviews.all()
        return Review.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReviewSerializerGet
        return ReviewSerializerPost

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(CustomMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [RoleCategory]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class GenreViewSet(CustomMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [RoleGenreOrTitle]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Round(Avg('reviews__score'))
    ).order_by('-rating')
    permission_classes = [RoleGenreOrTitle]
    filterset_class = TitleFilter
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'year', 'genre', 'category']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerGet
        return TitleSerializerPost
