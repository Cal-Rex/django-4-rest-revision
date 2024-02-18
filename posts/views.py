from django.shortcuts import render
from rest_framework import permissions, generics, filters #, status # obsolete when using generics
from rest_framework.response import Response
from django.db.models import Count
from drf_api.permissions import IsOwnerOrReadOnly
# from rest_framework.views import APIView # obsolete when using generics
from .models import Post
from .serializers import PostSerializer


# Create your views here.

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'comments_count'
        'likes_count'
        'likes__created_at'
    ]


    # this function needs to be added to bind a new post to a user /
    # assign a User key value to the "owner" field in the db
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # methods required if get and post functions written manually when
    # using the APIView template
    # def get(self, request):
    #     posts = Post.objects.all()
    #     serializer = PostSerializer(
    #         posts,
    #         many=True,
    #         context={'request': request}
    #     )
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = PostSerializer(
    #         data=request.data, context={'request': request}
    #     )
    #     if serializer.is_valid():
    #         serializer.save(owner=request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsOwnerOrReadOnly
    ]
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')

    # manual functions used if the APIView template is used
    # def get_object(self, pk):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, post)
    #         return post
    #     except Post.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(
    #         post,
    #         context={'request': request}
    #     )
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(
    #         post, data=request.data, context={'request': request}
    #     )
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #     )

    # def delete(self, request, pk):
    #     post = self.get_object(pk)
    #     post.delete()
    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT
    #     )