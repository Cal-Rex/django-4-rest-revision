from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    headline = serializers.ReadOnlyField
    publications = serializers.ReadOnlyField
    order = serializers.ReadOnlyField

    class Meta:
        model = Article
        fields = [
            'headline',
            'publications',
            'order',
        ]
