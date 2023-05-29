from django.contrib import admin
from .models import Property, Tip, Photo, Contact

# Register your models here.
admin.site.register(Property)
admin.site.register(Tip)
admin.site.register(Photo)
admin.site.register(Contact)
