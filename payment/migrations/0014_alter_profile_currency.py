# Generated by Django 5.1.6 on 2025-04-05 00:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_alter_profile_currency_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='payment.currency'),
        ),
    ]
