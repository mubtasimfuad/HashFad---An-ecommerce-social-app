# Generated by Django 4.1.1 on 2022-09-17 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]