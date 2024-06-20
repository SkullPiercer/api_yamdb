from django.urls import path
from .views import ObtainTokenView, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/', ObtainTokenView.as_view(), name='token'),
]

