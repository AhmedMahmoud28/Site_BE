from django.db import models

from userapp.models import User

# Create your models here.


class Package(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"


class Subscribe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.user}"


class SubscribeItem(models.Model):
    subscribe = models.ForeignKey(Subscribe, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subscribe} {self.package}"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.id} {self.user}"


class SubscriptionItem(models.Model):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="subscription_items"
    )
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    item_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.subscription} {self.package}"
