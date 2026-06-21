from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import MenuItem,Cart,CartItem,FoodOrder,FoodOrderItem,FoodAssignment
from .forms import CheckoutForm,FoodAssignmentForm,MenuItemForm

# Create your views here.
def menu(request):
    menu_items = MenuItem.objects.filter(
        available=True
    )
    return render(request,"grill/menu.html",{"menu_items":menu_items})

def add_to_cart(request,item_id):
    item = get_object_or_404(
        MenuItem,
        id=item_id
    )
    cart, created = Cart.objects.get_or_create(
        customer=request.user
    )
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        menu_item=item
    )
    if not created:
        cart_item.quantity +=1
    cart_item.save()
    return redirect("menu")

def cart_view(request):
    cart, created = Cart.objects.get_or_create(
        customer=request.user
    )

    total=0

    for item in cart.items.all():
        total +=(
            item.menu_item.price * item.quantity
        )
    return render(request,"grill/cart.html",{
        "cart":cart,
         "total":total
    })

@login_required
def checkout(request):
    cart = get_object_or_404(
        Cart,
        customer=request.user
    )

    if not cart.items.exists():
        return redirect("cart")
    form= CheckoutForm()

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = FoodOrder.objects.create(
                customer=request.user,
                delivery_address=form.cleaned_data["delivery_address"],
                notes=form.cleaned_data["notes"]
            )
            total=0

            for item in cart.items.all():
                FoodOrderItem.objects.create(
                    order=order,
                    menu_item=item.menu_item,
                    quantity=item.quantity
                )
                total +=(
                    item.menu_items.price * item.quantity
                )
                order.total_price = total
                order.save()

                cart.items.all().delete()

                return redirect("food_order_detail",pk=order.id)
            return render(request,"grill/checkout.html",{"cart":cart,"form":form})
        
@login_required
def food_order_detail(request,pk):
    order = get_object_or_404(
        FoodOrder,
        pk=pk
    )

    if order.customer != request.user:
        return redirect("dashboard")
    
    return render(request,"grill/food_order_detail.html",{"order":order})

@login_required
def food_order_list(request):

    orders = FoodOrder.objects.filter(
        customer=request.user
    ).order_by("-created_at")

    return render(
        request,
        "grill/food_order_list.html",
        {
            "orders": orders
        }
    )

@login_required
def assign_food_rider(request, pk):

    order = get_object_or_404(
        FoodOrder,
        pk=pk
    )

    assignment, created = (
        FoodAssignment.objects.get_or_create(
            order=order
        )
    )

    if request.method == "POST":

        form = FoodAssignmentForm(
            request.POST,
            instance=assignment
        )

        if form.is_valid():

            form.save()

            return redirect(
                "food_order_detail",
                pk=pk
            )

    else:

        form = FoodAssignmentForm(
            instance=assignment
        )

    return render(
        request,
        "grill/assign_food_rider.html",
        {
            "form": form,
            "order": order
        }
    )

@login_required
def update_food_status(
    request,
    pk,
    status
):

    order = get_object_or_404(
        FoodOrder,
        pk=pk
    )

    order.status = status

    order.save()

    return redirect(
        "food_order_detail",
        pk=pk
    )

@login_required
def menu_management(request):

    items = MenuItem.objects.all()

    return render(
        request,
        "grill/menu_management.html",
        {
            "items":items
        }
    )


@login_required
def add_menu_item(request):

    if request.method == "POST":

        form = MenuItemForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                "menu_management"
            )

    else:
        form = MenuItemForm()

    return render(
        request,
        "grill/add_menu_item.html",
        {
            "form":form
        }
    )


@login_required
def edit_menu_item(request, item_id):

    item = get_object_or_404(
        MenuItem,
        id=item_id
    )

    if request.method == "POST":

        form = MenuItemForm(
            request.POST,
            request.FILES,
            instance=item
        )

        if form.is_valid():

            form.save()

            return redirect(
                "owner_dashboard"
            )

    else:

        form = MenuItemForm(
            instance=item
        )

    return render(
        request,
        "grill/edit_menu_item.html",
        {
            "form": form,
            "item": item
        }
    )


@login_required
def delete_menu_item(request, item_id):

    item = get_object_or_404(
        MenuItem,
        id=item_id
    )

    if request.method == "POST":

        item.delete()

        return redirect(
            "owner_dashboard"
        )

    return render(
        request,
        "grill/delete_menu_item.html",
        {
            "item": item
        }
    )