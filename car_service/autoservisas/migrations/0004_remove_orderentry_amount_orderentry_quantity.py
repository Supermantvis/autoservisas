# Generated by Django 4.2.1 on 2023-06-02 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0003_car_car_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderentry',
            name='amount',
        ),
        migrations.AddField(
            model_name='orderentry',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='quantity'),
        ),
    ]
