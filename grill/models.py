from django.db import models
from django.conf import settings
from django .utils import timezone


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    description = models.TextField()
    image = models.ImageField(
        upload_to="menu_items/"
    )
    available = models.BooleanField(default=True)

    class Meta:
        db_table ="grill_menuitems"

    def __str__(self):
         return self.name

class FoodOrder(models.Model):
    STATUS_CHOICES = (
        ("pending","Pending"),
        ("preparing","Preparing"),
        ("ready","Ready"),
        ("delivery","Out of Delivery"),
        ("completed","Delivered"),
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    delivery_address = models.TextField()

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    total_price= models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Food Order #{self.id}"
    
class FoodOrderItem(models.Model):
        order = models.ForeignKey(
            FoodOrder,
            on_delete=models.CASCADE,
            related_name="items"
        )
        menu_item = models.ForeignKey(
            MenuItem,
            on_delete=models.CASCADE
        )
        quantity= models.PositiveIntegerField(
            default=1
        )
        def subtotal(self):
            return (
                self.menu_item.price* self.quantity
            )


class Cart(models.Model):
     customer = models.OneToOneField(
          settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE
     )
     created_at= models.DateTimeField(
        auto_now_add=True
     )
     def __str__(self):
          return f"{self.customer.username}'s Cart"
     
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE
    )
    quantity= models.PositiveIntegerField(
        default=1
    )
    def subtotal(self):
         return self.menu_item.price * self.quantity
    
    def __str__(self):
         return f"{self.quantity} * {self.menu_item.name}"

class FoodAssignment(models.Model):

    order = models.OneToOneField(
        FoodOrder,
        on_delete=models.CASCADE
    )

    rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="food_deliveries"
    )

    assigned_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return f"Food Order #{self.order.id}"
