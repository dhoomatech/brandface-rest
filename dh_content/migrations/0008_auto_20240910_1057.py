# Generated by Django 3.2.12 on 2024-09-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dh_content', '0007_alter_usergallery_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilelinks',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='profile/avatar/'),
        ),
        migrations.AlterField(
            model_name='profilelinks',
            name='background',
            field=models.ImageField(blank=True, upload_to='profile/background/'),
        ),
    ]
