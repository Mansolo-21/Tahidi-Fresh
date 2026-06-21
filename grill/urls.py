from django.urls import path
from .views import (menu,
add_to_cart,
cart_view,
checkout,
food_order_detail,
food_order_list,
assign_food_rider,
update_food_status,
menu_management,
add_menu_item,
edit_menu_item,
delete_menu_item)



urlpatterns = [
   path("",menu,name="menu"),
   path("add-to-cart/<int:item_id>/",add_to_cart,name="add_to_cart"),
   path("cart/",cart_view,name="cart"),
   path("checkout/",checkout,name="checkout"),
   path("orders/<int:pk>/",food_order_detail,name="food_order_detail"),
   path("orders/",food_order_list,name="food_order_list"),
   path("assign-rider/<int:pk>/",assign_food_rider,name="assign_food_rider"),
   path("order/<int:pk>/status/<str:status>/",update_food_status,name="update_food_status"),
   path(
    "menu/edit/<int:item_id>/",
    edit_menu_item,
    name="edit_menu_item"
    ),
    path(
        "menu/delete/<int:item_id>/",
        delete_menu_item,
        name="delete_menu_item"
    ),
    path("menu_management/",menu_management,name="menu_management"),
    path("add/",add_menu_item,name="add_menu_item")
]