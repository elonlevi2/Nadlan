from rest_framework import serializers
from ..models import Property, Photo, Tip, Contact
from django.contrib.auth.models import User


class PropertySerializers(serializers.ModelSerializer):
    """
    Serializer for the Property model.

    This serializer is used to convert Property model objects into a suitable data format for the API.
    It provides serialization and deserialization capabilities for Property objects.

    Serializer Fields:
        - All fields of the Property model are included.

    Example usage:
        serializer = PropertySerializers(data=request.data)
        if serializer.is_valid():
            property_object = serializer.save()
        else:
            errors = serializer.errors
    """

    class Meta:
        model = Property
        fields = "__all__"


class PhotoSerializers(serializers.ModelSerializer):
    """
    Serializer for the Photo model.

    This serializer is used to convert Photo model objects into a suitable data format for the API.
    It provides serialization and deserialization capabilities for Photo objects.

    Serializer Fields:
        - All fields of the Photo model are included.
    """

    class Meta:
        model = Photo
        fields = "__all__"


class TipSerializers(serializers.ModelSerializer):
    """
    Serializer for the Tip model.

    This serializer is used to convert Tip model objects into a suitable data format for the API.
    It provides serialization and deserialization capabilities for Tip objects.

    Serializer Fields:
        - All fields of the Tip model are included.
    """

    class Meta:
        model = Tip
        fields = "__all__"


class ContactSerializers(serializers.ModelSerializer):
    """
    Serializer for the Contact model.

    This serializer is used to convert Contact model objects into a suitable data format for the API.
    It provides serialization and deserialization capabilities for Contact objects.

    Serializer Fields:
        - All fields of the Contact model are included.
    """

    class Meta:
        model = Contact
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer is used to convert User model objects into a suitable data format for the API.
    It provides serialization and deserialization capabilities for User objects.

    Serializer Fields:
        - All fields of the User model are included.
    """

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ['password']
