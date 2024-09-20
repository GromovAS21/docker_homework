from rest_framework.validators import ValidationError


def url_validator(value):
    """
    Проверяет, является ли входящая ссылка на видео YouTube
    """
    if 'https://www.youtube.com/' not in value:
        raise ValidationError("Ссылка на видео может быть только с сайта YouTube")
