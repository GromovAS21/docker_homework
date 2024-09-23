from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from users.models import Payment, User
from users.permissions import IsUserProfile
from users.serializers import PaymentSerializer, UserSerializer, ProfileNotUserSerializer
from users.serivces import create_product, create_price, create_session


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Контроллер для получения списка всех пользователь"
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Контроллер для получения конкретного пользователя"
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Контроллер для создания пользователя"
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Контроллер для обновления информации о пользователе"
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Контроллер для частичного изменения информации о пользователе"
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Контроллер для удаления пользователя"
))
class UserViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для модели User
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Получаем права для действий
        """

        if self.action == "create":
            self.permission_classes = (AllowAny,)
        elif self.action == "list":
            self.permission_classes = (IsAdminUser, )
        elif self.action == "update":
            self.permission_classes = (IsUserProfile | IsUserProfile)
        elif self.action == "destroy":
            self.permission_classes = (IsUserProfile,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Создание нового пользователя с активным статусом
        """

        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_serializer_class(self):
        """
        В зависимости от действия возвращаем нужный сериализатор
        """

        if self.action == "retrieve":
            object = self.get_object()
            if self.request.user.id != object.id:
                return ProfileNotUserSerializer
        return UserSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Контроллер для получения списка всех оплат"
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Контроллер для получения конкретной оплаты"
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Контроллер для создания оплаты"
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Контроллер для обновления информации о оплате"
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Контроллер для частичного изменения информации об оплате"
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Контроллер для удаления оплаты"
))
class PaymentViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для модели Payment
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("payment_date",)
    filterset_fields = ("paid_course", "paid_lesson", "method")

    def perform_create(self, serializer):
        """
        Создание новой оплаты для текущего пользователя
        """

        payment = serializer.save(user=self.request.user)
        stripe_product = create_product(payment)
        stripe_price = create_price(payment, stripe_product)
        session_id, link = create_session(stripe_price)
        payment.session_id = session_id
        payment.link = link
        payment.save()


def success_pay(request):
    """
    Страница с успешной оплатой
    """
    return render(request, "users/success_pay.html")


