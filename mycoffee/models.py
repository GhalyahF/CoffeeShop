from django.db import models
from django.contrib.auth.models import User

class Bean(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name

class Roast(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name

class Syrup(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name

class Powder(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=3)

    def __str__(self):
        return self.name

class Coffee(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=120)
    espresso_shots = models.PositiveIntegerField(default=1)
    bean = models.ForeignKey(Bean)
    roast = models.ForeignKey(Roast)
    syrups = models.ManyToManyField(Syrup, blank=True)
    powders = models.ManyToManyField(Powder, blank=True)
    water = models.FloatField()
    steamed_milk = models.BooleanField(default=False)
    foam = models.FloatField()
    extra_instructions = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=3, null=True)

    def __str__(self):
        return self.name
