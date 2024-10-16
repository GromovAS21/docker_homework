# Generated by Django 5.1.1 on 2024-09-10 19:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0002_alter_lesson_description"),
        ("users", "0003_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="paid_course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments_course",
                to="materials.course",
                verbose_name="Оплаченный курс",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="paid_lesson",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments_lesson",
                to="materials.lesson",
                verbose_name="Оплаченный урок",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
    ]
