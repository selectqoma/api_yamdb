# Generated by Django 2.2.16 on 2021-10-13 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211013_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.UUIDField(default=0, editable=False, verbose_name='Код подтверждения'),
        ),
    ]
