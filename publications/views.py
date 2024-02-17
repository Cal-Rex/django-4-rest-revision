from django.shortcuts import render
from rest_framework import permissions, generics
from .models import Publication
from .serializers import PublicationSerializer

# Create your views here.
class PublicationList(generics.ListAPIView):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()

class PublicationDetail(generics.RetrieveAPIView):
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()