from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для модели User
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny,]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для модели Payment
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("payment_date",)
    filterset_fields = ("paid_course", "paid_lesson", "method")
