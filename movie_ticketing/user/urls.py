from django.urls import path

from .views import UserProfileCreateView

urlpatterns = [
    path("create/", UserProfileCreateView.as_view(), name="user_create"),
]
