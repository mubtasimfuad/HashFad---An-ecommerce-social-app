# Generated by Django 4.1.1 on 2022-10-01 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_deliverytask_isdelivered_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverytask',
            name='delivered_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
