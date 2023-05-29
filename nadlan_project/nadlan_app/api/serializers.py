from rest_framework import serializers
from ..models import Property, Photo, Tip, Contact
from django.contrib.auth.models import User


class PropertySerializers(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = "__all__"


class PhotoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = "__all__"


class TipSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tip
        fields = "__all__"


class ContactSerializers(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['password', 'username']

