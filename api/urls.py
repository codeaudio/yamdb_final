from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (CategoryViewSet, CommentViewSet,
                       CustomTokenObtainPairView, EmailViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet)

router_v1 = DefaultRouter()

router_v1.register('reviews', ReviewViewSet, basename='reviews')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('auth/email', EmailViewSet, basename='email')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path(
        'v1/auth/token/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/token/auth/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('v1/', include(router_v1.urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

