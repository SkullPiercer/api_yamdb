# Thirdparty imports
from django.urls import include, path

urlpatterns = [
    # path('v1/', include('authentificate.urls')),
    path('v1/', include('reviews.urls')),
]