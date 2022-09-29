# Generated by Django 4.1.1 on 2022-09-29 12:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('image', models.ImageField(blank=True, upload_to='photos/categories')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('phone1', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='BD')),
                ('phone2', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='BD')),
                ('username', models.CharField(blank=True, max_length=500, unique=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=4000)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('featured_image', models.ImageField(default='no.jpg', upload_to='photos/products')),
                ('is_available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='store.category')),
            ],
            options={
                'ordering': ('-modified_at',),
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('phone1', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='BD')),
                ('phone2', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='BD')),
                ('username', models.CharField(blank=True, max_length=500, unique=True)),
                ('store_name', models.CharField(max_length=300)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('nid', models.CharField(max_length=25)),
                ('licence_id', models.CharField(blank=True, max_length=25, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendor_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=100)),
                ('review', models.TextField(blank=True, max_length=500)),
                ('rating', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('query', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='query_reply', to='store.query')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='query', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='photos/products')),
                ('stock', models.PositiveIntegerField()),
                ('added_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('color', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('size', models.CharField(choices=[('32', '32'), ('34', '34'), ('36', '36'), ('38', '38'), ('40', '40'), ('42', '42'), ('44', '44'), ('46', '46'), ('default', 'Default')], default='default', max_length=20, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='store.product')),
            ],
            options={
                'unique_together': {('product', 'color', 'size')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.vendor'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placed_at', models.DateTimeField(auto_now_add=True)),
                ('delivery_status', models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('returned', 'Returned')], default='pending', max_length=25)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', max_length=25)),
                ('payment_method', models.CharField(choices=[('cod', 'Cash On Delivery'), ('op', 'Online Payment')], default=None, max_length=25, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.productvariation')),
            ],
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='store.basket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productvariation')),
            ],
            options={
                'unique_together': {('basket', 'product')},
            },
        ),
    ]
