# Generated by Django 2.2.16 on 2021-10-15 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0006_title_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.PositiveIntegerField(null=True, verbose_name='Рейтинг'),
        ),
    ]
