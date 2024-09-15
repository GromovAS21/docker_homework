from django.db import models


class Course(models.Model):
    """
    Модель курса
    """

    title = models.CharField(
        max_length=50,
        verbose_name="Название курса",
    )
    description = models.TextField(
        verbose_name="Описание курса",
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='course/',
        verbose_name="Превью курса",
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Владелец курса",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = ("Курс",)
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Модель урока
    """

    course = models.ForeignKey(
        Course,
        verbose_name="Курс",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока"
    )
    description = models.TextField(
        verbose_name="Описание урока",
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='course/',
        verbose_name="Превью урока",
        blank=True,
        null=True
    )
    url_video = models.CharField(
        max_length=200,
        verbose_name="Ссылка на видео",
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        verbose_name="Владелец урока",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ("id",)

    def __str__(self):
        return self.title
