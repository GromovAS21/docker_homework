from rest_framework import serializers

from users.models import User, Payment


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment
    """
    class Meta:
        model = Payment
        fields = "__all__"


