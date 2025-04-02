from django.db import models
from django.contrib.auth.models import User



class Currency(models.Model):
    code=models.CharField(max_length=3)
    name=models.CharField(max_length=50)
    value=models.DecimalField(default=1,max_digits=10, decimal_places=2)
    def __str__(self):
        return self.code




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=750)
    admin = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


class Pay(models.Model):
    payer=models.CharField(max_length=10)
    payee=models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} by {self.user}"

