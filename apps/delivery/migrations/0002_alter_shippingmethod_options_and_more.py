# Generated by Django 4.2.7 on 2023-12-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippingmethod',
            options={'ordering': ['default', '-created_at']},
        ),
        migrations.AddField(
            model_name='shippingmethod',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='shippingmethod',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]