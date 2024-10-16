from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment
    """

    class Meta:
        model = Payment
        exclude = ("status",)


class PaymentStatusSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment
    """

    class Meta:
        model = Payment
        fields = ("payment_date", "amount", "paid_course", "paid_lesson", "status",)


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """

    payments = PaymentSerializer(source="users", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class ProfileNotUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User если осуществляется просмотр чужого профиля
    """
    class Meta:
        model = User
        exclude = ("password", "last_name")
