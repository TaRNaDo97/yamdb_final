from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentViewSet, EmailRegistrationView,
                    GenreViewSet, GetTokenView, RewievViewSet, TitleViewSet,
                    UserViewSet)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[^/d]+)/reviews',
    RewievViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[^/d]+)/reviews/(?P<review_id>[^/d]+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/token/', GetTokenView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/auth/email/', EmailRegistrationView.as_view()),
    path('v1/', include(router.urls)),
]
