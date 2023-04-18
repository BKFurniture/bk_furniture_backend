from django.contrib import admin
from django.contrib import messages

import requests

from .models import Coupon


@admin.action(description="Issue coupons by user emails")
def make_issued(modeladmin, request, queryset):
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json"
    }
    for obj in queryset:
        user_emails = []
        for user in obj.selected_users.all():
            user_emails.append(user.email)
        payload = {
            "discountCode": obj.code,
            "discountPercentage": obj.discount,
            "usageLimit": obj.usage_limit,
            "userMails": user_emails
        }
        res = requests.post(
            "https://bkfurniturebackendmailer-production.up.railway.app/mailer/sale",
            json=payload,
            headers=headers
        )
        print(res.content)
        # Error Handling
    messages.info(request, "Issued the coupons successfully!")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("id", "is_active", "code", "discount", "usage_limit")
    actions = [make_issued]
