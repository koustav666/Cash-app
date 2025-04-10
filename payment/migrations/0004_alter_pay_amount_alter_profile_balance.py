# Generated by Django 5.1.6 on 2025-03-19 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_pay_amount_alter_profile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=750, max_digits=10),
        ),
    ]
