from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'
    def ready(self):
        from django.contrib.auth.models import User
        from payment.models import Profile, Currency

        def create_superuser_currency(sender, **kwargs):
            defaults = [
                {"code": "GBP", "name": "British Pound", "value": 1},
                {"code": "USD", "name": "US Dollar", "value": 1.3},
                {"code": "EUR", "name": "Euro", "value": 1.2},
            ]

            for entry in defaults:
                Currency.objects.get_or_create(code=entry["code"], defaults={
                    "name": entry["name"],
                    "value": entry["value"]
                })
            if not User.objects.filter(username='admin1').exists():
                User.objects.create_superuser(
                    username='admin1',
                    email='admin1@example.com',
                    password='admin1'  # change this in production!
                )
                Profile.objects.create(
                    user=User.objects.get(username='admin1'),
                    balance=1000,
                    admin=True,
                    currency=Currency.objects.get(code="GBP")
                )
            
        post_migrate.connect(create_superuser_currency, sender=self)