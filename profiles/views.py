from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.
class ProfileList(APIView):
    """view that lists all the profiles
    stored in the db"""
    serializer_class = ProfileSerializer
        # serializes the update form
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProfileDetail(APIView):
    # establish the form structure for the data
    serializer_class = ProfileSerializer

    def get_object(self, pk):
        """
        the function that checks the validity
        of a profile request, returns an error if
        invalid
        """
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        """
        uses the function above to get a profile by id
        serializes it using the ProfileSerializer
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        updates a retreived profile with data receieved
        from a request via a form contextualised by
        serializer_class at the top of this view
        handles BAD_REQUEST errors too
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
