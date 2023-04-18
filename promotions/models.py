from django.db import models
from django.contrib.auth.models import User


class Coupon(models.Model):
    code = models.CharField(max_length=63, unique=True)
    discount = models.PositiveSmallIntegerField()
    usage_limit = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    selected_users = models.ManyToManyField(
        User,
        related_name="issued_coupons",
        blank=True)
    user_blocklist = models.ManyToManyField(
        User,
        related_name="used_coupons",
        blank=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        return self.is_active and self.usage_limit > 0

    def is_valid_user(self, user):
        return user in self.selected_users.all() and user not in self.user_blocklist.all()

    def decrease_usage_limit(self):
        self.usage_limit -= 1 if self.usage_limit > 0 else 0
        self.save()
        return self.usage_limit

    def add_user_blocklist(self, user):
        return self.user_blocklist.add(user)
