# Generated by Django 4.2.11 on 2024-04-03 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20240402_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.CharField(max_length=10),
        ),
    ]