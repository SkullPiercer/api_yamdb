from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('api/v1/auth/token/', ..., name='token'),
]

