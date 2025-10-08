from django.db import models
from django.utils import timezone


class Company(models.Model):
    """
    Represents a business account using WhatsSale.
    Each company belongs to one owner (User with role='owner').
    """

    # Basic info
    name = models.CharField(max_length=150)
    owner = models.OneToOneField(
        "accounts.User", on_delete=models.CASCADE, related_name="owned_company"
    )
    industry = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Contact info
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    timezone = models.CharField(max_length=50, default="America/Bogota")

    # WhatsApp Cloud API configuration (per company)
    whatsapp_business_id = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_phone_id = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_access_token = models.TextField(blank=True, null=True)

    # Subscription / billing info
    subscription_plan = models.CharField(
        max_length=50,
        choices=[
            ("free", "Free"),
            ("basic", "Basic"),
            ("pro", "Pro"),
            ("enterprise", "Enterprise"),
        ],
        default="free",
    )

    subscription_status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("trial", "Trial"),
            ("suspended", "Suspended"),
            ("cancelled", "Cancelled"),
        ],
        default="trial",
    )
    
    subscription_expires_at = models.DateTimeField(blank=True, null=True)

    # Operational status and audit
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_subscription_active(self):
        if not self.subscription_expires_at:
            return False
        return self.subscription_expires_at > timezone.now()

    def plan_label(self):
        return self.get_subscription_plan_display()
