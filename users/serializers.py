from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment
    """

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """

    payments = PaymentSerializer(source="users", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
