from django.contrib import admin
from .models import Rating, RatingImage


@admin.register(RatingImage)
class RatingImageAdmin(admin.ModelAdmin):
    list_display = ("id", "rating")


class RatingImageInline(admin.TabularInline):
    model = RatingImage
    extra = 0


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("order_item", "user", "stars", "comment",
                    "created_at", "updated_at")
    inlines = [RatingImageInline]


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
