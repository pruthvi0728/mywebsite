# Generated by Django 3.0.2 on 2020-01-31 13:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_chatboard_cbmsgbyadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatboard',
            name='cbdatetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]