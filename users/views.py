from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для модели User
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для модели Payment
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("payment_date",)
    filterset_fields = ("paid_course", "paid_lesson", "method")
