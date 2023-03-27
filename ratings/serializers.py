from rest_framework import serializers

from users.serializers import UserSerializer
from ratings.models import Rating, RatingImage
from datetime import datetime

class RatingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingImage
        fields = [
            "url",
        ]


class RatingSerializer(serializers.ModelSerializer):
    images = RatingImageSerializer(many=True, read_only=True, required=False)
    user = UserSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = Rating
        fields = [
            "id",
            "stars",
            "comment",
            "created_at",
            "updated_at",
            "user",
            "images",
        ]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        # rating_user = instance.user
        # request_user = self.context['request'].user
        # if rating_user != request_user:
        #     raise serializers.ValidationError("You do not have permission to edit this rating")

        stars = validated_data.get('stars', instance.stars)
        comment = validated_data.get('comment', instance.comment)

        setattr(instance, 'stars', stars)
        setattr(instance, 'comment', comment)
        setattr(instance, 'updated_at', datetime.now())
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        instance.save()
        return instance
