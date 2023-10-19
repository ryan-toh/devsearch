# serializer
from rest_framework import serializers

# model to serialize
from projects.models import Project, Tag, Review
from users.models import Profile


# converts model to a JSON object
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    # OVERRIDING THE SERIALIZER
    # only one owner, thus many=False
    owner = ProfileSerializer(many=False)
    # we want all the tags, hence many=True
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    # start all functions with "get_" (according to django docs)
    # after getting the data, it will be passed into the SerializerMethodField
    def get_reviews(self, obj):
        # get all the projects' reviews
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


    class Meta:
        model = Project
        fields = "__all__"


