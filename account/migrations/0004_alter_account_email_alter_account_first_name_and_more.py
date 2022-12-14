# Generated by Django 4.1.2 on 2022-10-10 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_activatorkey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='account',
            name='user_type',
            field=models.CharField(choices=[('agent', 'Agent'), ('vendor', 'Vendor'), ('customer', 'Customer')], max_length=250),
        ),
    ]
