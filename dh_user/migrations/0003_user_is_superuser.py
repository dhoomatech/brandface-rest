# Generated by Django 3.2.12 on 2024-07-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dh_user', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
