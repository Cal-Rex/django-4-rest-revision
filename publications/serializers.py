from rest_framework import serializers
from .models import Publication

class PublicationSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField

    class Meta:
        model = Publication
        fields = [
            'title',
        ]
