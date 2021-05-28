# Generated by Django 3.2 on 2021-05-18 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210510_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer_address', to='accounts.customerprofile')),
            ],
        ),
    ]
