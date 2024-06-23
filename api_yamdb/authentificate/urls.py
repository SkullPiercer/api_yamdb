from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MeDetailView, ObtainTokenView, SignUpView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', ObtainTokenView.as_view(), name='token'),
    path('users/me/', MeDetailView.as_view(), name='me-detail'),
    path('', include(router.urls)),
]
