from django.shortcuts import render
# from rest_framework.views import APIView # obsolete when using the generics import below
from rest_framework import generics, filters
from rest_framework.response import Response
from django.db.models import Count
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.
class ProfileList(generics.ListAPIView):
    """view that lists all the profiles
    stored in the db"""
    serializer_class = ProfileSerializer
        # serializes the update form
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        'posts_count',
        'followed_count',
        'following_count',
        'owner__followed__created_at',
        'owner__following__created_at',
        ]

    # manual view method if using the APIView view from rest framework
    # def get(self, request):
    #     profiles = Profile.objects.all()
    #     serializer = ProfileSerializer(profiles, many=True, context={'request': request})
    #     return Response(serializer.data)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    # establish the form structure for the data
    serializer_class = ProfileSerializer
    # establish the permissions for the data
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()

    # manual methods of writing vew if using APIView template
    # def get_object(self, pk):
    #     """
    #     the function that checks the validity
    #     of a profile request, returns an error if
    #     invalid
    #     """
    #     try:
    #         profile = Profile.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, profile)
    #         return profile
    #     except Profile.DoesNotExist:
    #         raise Http404
    # def get(self, request, pk):
    #     """
    #     uses the function above to get a profile by id
    #     serializes it using the ProfileSerializer
    #     """
    #     profile = self.get_object(pk)
    #     serializer = ProfileSerializer(profile, context={'request': request})
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     """
    #     updates a retreived profile with data receieved
    #     from a request via a form contextualised by
    #     serializer_class at the top of this view
    #     handles BAD_REQUEST errors too
    #     """
    #     profile = self.get_object(pk)
    #     serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
