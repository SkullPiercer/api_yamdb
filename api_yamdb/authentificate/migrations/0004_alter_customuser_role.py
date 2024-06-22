# Generated by Django 3.2 on 2024-06-21 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentificate', '0003_auto_20240619_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')], max_length=50),
        ),
    ]