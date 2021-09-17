# Create your models here.
import secrets
from django.db import models
from django.db.models.fields import CharField
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import User


CATEGORY = (
    ('W', 'WAEC'),
    ('N', 'NECO'),
    ('J', 'JAMB')
)

LABEL = (
    ('I', 'In-stock'),
    ('O', 'Out-of-stock')
)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True, db_index=True)
    category = models.CharField(choices=CATEGORY, max_length=1)
    label = models.CharField(choices=LABEL, max_length=1)
    updated_at = models.DateTimeField(auto_now_add=True, db_index=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='picture/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_image_url(self):
        return self.image.url

    #def get_absolute_url(self):
     #  return reverse('detail', args=[str(self.id)])

    #def get_absolute_url(self):
     #   return reverse('detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.id) + " CartProduct: " + str(self.id)

METHOD = (
    ('Interswitch', 'Interswitch'),
    ('Paystack', 'Paystack'),
)

class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    mobile = models.CharField(max_length=11)
    email = models.EmailField(null=True)
    ref = models.CharField(max_length=200)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    payment_method = models.CharField(max_length=20, choices=METHOD, default='Interswtich')
    payment_completed = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_ref = Order.objects.filter(ref=ref)
            if not obj_ref:
                self.ref = ref
        super().save(*args, **kwargs)
