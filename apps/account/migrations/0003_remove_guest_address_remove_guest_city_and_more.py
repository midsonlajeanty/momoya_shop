# Generated by Django 4.2.7 on 2023-12-13 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_guest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='address',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='city',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='country',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='state',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='zipcode',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zipcode', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]