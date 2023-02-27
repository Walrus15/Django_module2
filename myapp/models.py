from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    bank = models.FloatField(default='0.0')


class Product(models.Model):
    title = models.CharField(max_length=119)
    description = models.TextField(max_length=250, null=True, blank=True)
    price = models.FloatField(default=0, null=False)
    stock = models.IntegerField(null=False)

    def __str__(self):
        return self.title

class Purchase(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantily = models.IntegerField()
    time_purchase = models.DateTimeField(auto_now_add=True)

class Return(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    time_return = models.DateTimeField(auto_now_add=True)