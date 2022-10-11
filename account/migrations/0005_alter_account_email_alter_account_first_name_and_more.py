# Generated by Django 4.1.2 on 2022-10-10 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_account_email_alter_account_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='account',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='account',
            name='user_type',
            field=models.CharField(choices=[('agent', 'Agent'), ('vendor', 'Vendor'), ('customer', 'Customer')], max_length=25),
        ),
        migrations.AlterField(
            model_name='activatorkey',
            name='activation_key',
            field=models.CharField(max_length=10),
        ),
    ]