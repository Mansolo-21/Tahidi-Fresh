from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("shopper", "Shopper"),
        ("rider","Rider"),
        ("admin","Admin,"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer"
    )

    can_shop=models.BooleanField(
        default=False
    )
    can_deliver = models.BooleanField(
        default=False
    )