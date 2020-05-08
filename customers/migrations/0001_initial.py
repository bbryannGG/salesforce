# Generated by Django 2.2.7 on 2020-05-08 12:20

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
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyName', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=12)),
                ('phone2', models.CharField(blank=True, max_length=12)),
                ('contactPerson', models.CharField(max_length=50)),
                ('contactPerson2', models.CharField(blank=True, max_length=50)),
                ('addressLine1', models.CharField(max_length=100)),
                ('addressLine2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('postalCode', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=50)),
                ('website', models.CharField(blank=True, max_length=100)),
                ('additionalInfo', models.TextField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_created', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('export_customer', 'Can export customer data as excel file')],
            },
        ),
    ]
