from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserProfileCreateView

urlpatterns = [
    path("create/", UserProfileCreateView.as_view(), name="user_create"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
