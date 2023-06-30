from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Property(models.Model):
    location = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    price = models.PositiveIntegerField(null=False, blank=False)
    size = models.PositiveIntegerField(null=False, blank=False)
    rooms = models.CharField(null=False, blank=False, max_length=4)
    balcony = models.CharField(max_length=10, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    type = models.CharField(max_length=10, null=False, blank=False)
    real_estate = models.ForeignKey(related_name="property_user", null=False, on_delete=models.CASCADE, to=User)
    phone = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return f"{self.id} - {self.address}, real estate: {self.real_estate.id}"

    class Meta:
        db_table = 'Property'


class Tip(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(null=False, blank=False, max_length=2000)
    real_estate = models.ForeignKey(related_name="tip_user", null=False, on_delete=models.CASCADE, to=User)

    def __str__(self):
        return f"{self.id} - {self.title}"

    class Meta:
        db_table = 'Tip'


class Photo(models.Model):
    image = models.CharField(null=False, blank=False, max_length=20)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos')

    def __str__(self):
        return f"photo id:{self.id} - property:{self.property}"

    class Meta:
        db_table = 'Photo'


class Contact(models.Model):
    name = models.CharField(null=False, max_length=50)
    email = models.EmailField(null=False, blank=False)
    message = models.CharField(null=False, blank=False, max_length=2000)

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        db_table = 'Contact'
