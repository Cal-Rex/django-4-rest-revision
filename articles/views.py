from django.shortcuts import render
from rest_framework import permissions, generics
from .models import Article
from .serializers import ArticleSerializer

# Create your views here.
class ArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

class ArticleDetail(generics.RetrieveAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
