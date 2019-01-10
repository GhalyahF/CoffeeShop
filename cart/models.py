from django.db import models
from mycoffee.models import Coffee
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete


class CartItem(models.Model):
    cart= models.ForeignKey("Cart", on_delete= models.CASCADE)
    item= models.ForeignKey(Coffee, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(decimal_places = 3, max_digits = 20)

    def __str__(self):
        return self.item.title

def cart_item_receiver(sender,instance, *args, **kwargs):
    qty= instance.quantity
    if qty:
        price = instance.item.price
        line_item_total= price * int(qty)
        instance.line_item_total= line_item_total

pre_save.connect(cart_item_receiver, sender=CartItem)

def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete= models.CASCADE)
    items = models.ManyToManyField(Coffee, through=CartItem)
    subtotal = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)
    delivery_total = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)
    total = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)

    def __str__(self):
        return str(self.id)

    def update_subtotal(self):
        subtotal=0
        items= self.cartitem_set.all()
        for item in items:
            subtotal += item.line_item_total
        self.subtotal = subtotal
        self.save()

def delivery_and_total(sender, instance, *args, **kwargs):
    subtotal= instance.subtotal
    delivery_total= 2
    total= subtotal+delivery_total
    instance.delivery_charge= delivery_total
    instance.total = total

pre_save.connect(delivery_and_total, sender= Cart)



class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    block = models.CharField(max_length=3)
    avenue = models.PositiveIntegerField(blank=True, null=True)
    street = models.CharField(max_length=255)
    building_number = models.PositiveIntegerField()
    floor = models.CharField(max_length=3, null=True, blank=True)
    apt_number = models.PositiveIntegerField(null=True, blank=True)
    extra_directions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.email)
