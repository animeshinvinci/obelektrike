# Generated by Django 2.0.3 on 2018-03-31 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_auto_20180331_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='is_published',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Опубликован?'),
        ),
    ]