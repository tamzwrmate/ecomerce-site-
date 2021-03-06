# Generated by Django 3.2.7 on 2021-09-08 11:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('category', models.CharField(choices=[('W', 'WAEC'), ('N', 'NECO'), ('J', 'JAMB')], max_length=1)),
                ('label', models.CharField(choices=[('I', 'In-stock'), ('O', 'Out-of-stock')], max_length=1)),
                ('updated_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='picture/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_by', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('ref', models.CharField(max_length=200)),
                ('subtotal', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('payment_method', models.CharField(choices=[('Interswitch', 'Interswitch'), ('Paystack', 'Paystack')], default='Interswtich', max_length=20)),
                ('payment_completed', models.BooleanField(blank=True, default=False, null=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pinmall.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('subtotal', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinmall.cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pinmall.item')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pinmall.customer'),
        ),
    ]
