# Generated by Django 5.1.6 on 2025-03-28 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_profile_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=50)),
                ('value', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
            ],
        ),
    ]
