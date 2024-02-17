from rest_framework import serializers
from .models import Post
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.id')
    profile_image = serializers.ReadOnlyField(source='owner.image.url')
    is_owner = serializers.SerializerMethodField()
    like_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        # the like_id variable is prefixed with get_ to run
        # a specific method type
        user = self.context['request'].user
        # the user variable gets the user that 
        # prompted the method to run
        if user.is_authenticated:
            # checks if the user is authenticated 
            # if they are:
            liked = Like.objects.filter(owner=user, post=obj).first()
                # the liked variable runs on each entry in Post
                # and checks is a user is the owner of a like for that post
            print(liked)
                # just a print statement to check its all kushty in the CLI
            return liked.id if liked else None
                # for each entry, the serializer will return the id of the like
                # created for that post by that authenticated user
                # if the user hasnt made one, the method will return a "None" value
        return None
            # skip to end if user isnt authenticated and return "None" for all Posts

    class Meta:
        model = Post
        fields = [
            'id',
            'owner',
            'profile_id',
            'profile_image',
            'created_at',
            'updated_at',
            'title',
            'content',
            'image',
            'is_owner',
            'like_id',
        ]
