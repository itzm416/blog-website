# Generated by Django 4.0.1 on 2022-02-01 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0009_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='verify',
        ),
    ]
