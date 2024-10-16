from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet, success_pay

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

    path('success_pay/', success_pay, name="success_pay")
] + router.urls




