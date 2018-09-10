from rest_framework import serializers
from .models import Request

class RequestSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Request
        fields = ('id', 'string', 'date_created','date_modified')
        read_only_fields = ('date_created','date_modified')



from django.test import TestCase