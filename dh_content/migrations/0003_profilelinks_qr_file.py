# Generated by Django 3.2.12 on 2024-08-17 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dh_content', '0002_profilelinks_background_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilelinks',
            name='qr_file',
            field=models.FileField(blank=True, upload_to='qr-code'),
        ),
    ]