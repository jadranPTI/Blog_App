
# from django.contrib import admin
from django.urls import path
from .views import UserLoginAPIView, UserCreateAPIView

app_name = "accounts"

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login', UserLoginAPIView.as_view(), name="login"),
    path('create-user', UserCreateAPIView.as_view(), name="create_user")
]
