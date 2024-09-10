from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


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
    ordering_fields = ('payment_date',)
    filterset_fields = ('paid_course', 'paid_lesson', 'method')




