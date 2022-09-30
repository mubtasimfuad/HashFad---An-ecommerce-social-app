# Generated by Django 4.1.1 on 2022-09-29 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_status',
        ),
        migrations.RemoveField(
            model_name='order',
            name='placed_at',
        ),
        migrations.AddField(
            model_name='order',
            name='invoice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='store.invoice'),
            preserve_default=False,
        ),
    ]