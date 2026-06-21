from  django.conf import settings 
from django.db import models

class ShoppingRequest(models.Model):
    STATUS_CHOICES = (
        ("pending","Pending"),
        ("assigned","Assigned"),
        ("shopping","Shopping"),
        ("payment","Awaiting Payment"),
        ("delivery","Out For Delivery"),
        ("completed","Delivered"),
    )
    SUPERMARKET_CHOICES= (
        ("carrefour","Carrefour"),
        ("naivas","Naivas"),
        ("quickmart","Quickmart"),
        ("chandarana","Chandarana"),
        ("other","Other"),
    )

    customer= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    supermarket = models.CharField(max_length=100,
                                   choices=SUPERMARKET_CHOICES)

    delivery_address = models.TextField()

    shopping_list = models.FileField(
        upload_to="shopping_lists/",blank=True,null=True
    )

    shopping_list_text=models.TextField(blank=True)

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"{self.customer.username} - {self.supermarket}"

class Assignment(models.Model):

    request = models.OneToOneField(
        ShoppingRequest,
        on_delete=models.CASCADE
    )
    shopper= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="shopping_jobs",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    rider=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="delivery_jobs",
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    assigned_at=models.DateTimeField(
        auto_now_add=True
    )
    def __str__(self):
        return f"Assignment for Request {self.request.id}"
    
class Activity(models.Model):
    request = models.ForeignKey(
        ShoppingRequest,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    description = models.CharField(
        max_length=255
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.description