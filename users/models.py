from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """
    Модель пользователя
    """

    username = None

    email = models.EmailField(
        max_length=50,
        verbose_name="Email",
        unique=True,
    )
    telephone = models.PositiveIntegerField(
        verbose_name="Номер телефона",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
    )
    avatar = models.ImageField(
        upload_to="users/",
        verbose_name="Аватар",
        blank=True,
        null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.email


class Payment(models.Model):
    """
    Модель Платежа
    """
    STATUS_CHOICES = [
        ("Наличные", "Наличные"),
        ("Перевод на счет", "Перевод на счет")
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True,
        related_name="users",
    )
    payment_date = models.DateTimeField(
        verbose_name="Дата платежа",
        auto_now_add=True,
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        null=True,
        blank=True,
        related_name="payments_course",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        null=True,
        blank=True,
        related_name="payments_lesson",
    )
    amount = models.IntegerField(
        verbose_name="Сумма платежа",
    )
    method = models.CharField(
        choices=STATUS_CHOICES,
        default="Перевод на счет",
        max_length=50,
        verbose_name="Метод оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="ID сессии",
        blank=True,
        null=True,
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("-payment_date",)

    def __str__(self):
        return f"{self.paid_course if self.paid_course else self.paid_lesson} - {self.payment_date} ({self.user})"
