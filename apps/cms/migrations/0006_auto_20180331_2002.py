# Generated by Django 2.0.3 on 2018-03-31 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_poll_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seopage',
            name='url',
            field=models.CharField(max_length=255, unique=True, verbose_name='Относительный адрес'),
        ),
    ]