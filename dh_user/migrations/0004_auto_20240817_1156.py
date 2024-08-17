# Generated by Django 3.2.12 on 2024-08-17 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dh_user', '0003_user_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofiledata',
            name='about',
        ),
        migrations.RemoveField(
            model_name='userprofiledata',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='userprofiledata',
            name='category',
        ),
        migrations.RemoveField(
            model_name='userprofiledata',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='userprofiledata',
            name='description',
        ),
        migrations.RemoveField(
            model_name='userprofiledata',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='userprofiledata',
            name='is_ass_admin',
        ),
        migrations.RemoveField(
            model_name='userprofiledata',
            name='website',
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
