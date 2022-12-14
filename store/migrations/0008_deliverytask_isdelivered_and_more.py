# Generated by Django 4.1.1 on 2022-10-01 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_deliverytask'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverytask',
            name='isDelivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='deliverytask',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='deliverytask',
            name='delivery_time',
            field=models.DateField(),
        ),
    ]
