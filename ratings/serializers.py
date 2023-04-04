from rest_framework import serializers
from datetime import datetime


from ratings.models import Rating, RatingImage
from orders.models import OrderItem, Order
from users.serializers import ProfileSerializer
from users.models import Profile


class RatingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingImage
        fields = [
            "url",
        ]


class RatingSerializer(serializers.ModelSerializer):
    images = RatingImageSerializer(many=True, read_only=True, required=False)
    order_item = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Rating
        fields = [
            "stars",
            "comment",
            "created_at",
            "updated_at",
            "order_item",
            "images",
            "user"
        ]
        read_only_fields = ["order_item", "created_at", "updated_at", "user"]

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


class RatingDisplaySerializer(RatingSerializer):
    class Meta:
        model = Rating
        fields = [
            "stars",
            "comment",
            "is_updated",
            "user",
            "images",
        ]

    is_updated = serializers.SerializerMethodField()

    def get_is_updated(self, ob):
        return ob.updated_at != ob.created_at
