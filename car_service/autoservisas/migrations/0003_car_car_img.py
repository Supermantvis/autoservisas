# Generated by Django 4.2.1 on 2023-06-02 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisas', '0002_alter_carmodel_year_alter_orderentry_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='car_img',
            field=models.ImageField(blank=True, null=True, upload_to='autoservisas/car_images', verbose_name='car_img'),
        ),
    ]