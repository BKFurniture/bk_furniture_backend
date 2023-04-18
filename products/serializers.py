from rest_framework import serializers

from django.db.models import Avg
from decimal import Decimal

from products.models import Product, ProductImage, CustomDesign, CustomDesignImage, Category
from ratings.serializers import RatingSerializer, RatingDisplaySerializer
from users.serializers import UserSerializer


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            "url",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    images = ProductImageSerializer(many=True, read_only=True, required=False)
    # ratings = RatingDisplaySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id',
                  'name',
                  'slug',
                  'category',
                  'price',
                  'description',
                  'origin',
                  'colors',
                  'sizes',
                  'is_custom_design',
                  'category',
                  'images',
                  'avg_rating',
                  'count_rating',
                  ]
        read_only_fields = ['id']
    avg_rating = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, ob):
        stars_avg = ob.ratings.all().aggregate(Avg('stars'))['stars__avg']
        return stars_avg if stars_avg else Decimal(0.0)

    def get_count_rating(self, ob):
        count_rating = ob.ratings.all().count()
        return count_rating


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    images = ProductImageSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "price",
            "description",
            "origin",
            "colors",
            "sizes",
            "is_custom_design",
            "images",
            "avg_rating",
            "count_rating",
        ]

    avg_rating = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, ob):
        stars_avg = ob.ratings.all().aggregate(Avg('stars'))['stars__avg']
        return stars_avg if stars_avg else Decimal(0.0)

    def get_count_rating(self, ob):
        count_rating = ob.ratings.all().count()
        return count_rating


class CustomDesignImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomDesignImage
        fields = [
            "url",
        ]


class CustomDesignSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    custom_design_images = CustomDesignImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=False,
            use_url=False
        ),
        write_only=True
    )

    class Meta:
        model = CustomDesign
        fields = [
            "user",
            "description",
            "custom_design_images",
            "uploaded_images"
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        custom_design = CustomDesign.objects.create(**validated_data)
        for image in uploaded_images:
            CustomDesignImage.objects.create(custom_design=custom_design, url=image)
        return custom_design


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ProductImageCreateSerializer(serializers.ModelSerializer):
    urls = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=False,
            use_url=False
        ),
        write_only=True
    )

    class Meta:
        model = ProductImage
        fields = [
            "product",
            "urls"
        ]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("urls")
        for image in uploaded_images:
            product_image = ProductImage.objects.create(**validated_data)
            product_image.url = image
            product_image.save()
        return product_image
