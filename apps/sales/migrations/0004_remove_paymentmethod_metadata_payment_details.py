# Generated by Django 4.2.7 on 2023-12-13 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_alter_paymentmethod_options_paymentmethod_available_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentmethod',
            name='metadata',
        ),
        migrations.AddField(
            model_name='payment',
            name='details',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
