from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseForbidden
from accounts.models import User
from django.db.models import Sum
from shopping.models import (
    ShoppingRequest,
    Assignment
)

from grill.models import (
    FoodOrder,
    FoodAssignment,
    MenuItem
)

from django.db.models import Sum

# Create your views here.
def home(requests):
    return render(requests,"core/home.html")

login_required
def dashboard(request):
    return render(request,"core/dashboard.html")

@login_required
def owner_dashboard(request):
    if request.user.role != "admin":
        return HttpResponseForbidden(
            "You are not authorized."
        )

    menu_items = MenuItem.objects.all()
    total_requests = (
        ShoppingRequest.objects.count()
    )

    pending_requests = (
        ShoppingRequest.objects.filter(
            status="pending"
        ).count()
    )

    active_deliveries = (
        ShoppingRequest.objects.filter(
            status="delivery"
        ).count()
    )

    food_orders = (
        FoodOrder.objects.count()
    )

    active_food_deliveries = (
        FoodOrder.objects.filter(
            status="delivery"
        ).count()
    )

    total_food_revenue = (
    FoodOrder.objects.filter(
        status="completed"
    )
    .aggregate(total=Sum("total_price"))
    ["total"]
    or 0
)

    return render(
        request,
        "dashboard/owner_dashboard.html",
        {
            "total_requests": total_requests,
            "pending_requests": pending_requests,
            "active_deliveries": active_deliveries,
            "food_orders": food_orders,
            "active_food_deliveries":
                active_food_deliveries,
            "total_food_revenue":
                total_food_revenue,
            "menu_items": menu_items
        }
    )

@login_required
def rider_dashboard(request):

    shopping_jobs = Assignment.objects.filter(
        rider=request.user
    )

    food_jobs = FoodAssignment.objects.filter(
        rider=request.user
    )

    return render(
        request,
        "core/rider_dashboard.html",
        {
            "shopping_jobs": shopping_jobs,
            "food_jobs": food_jobs
        }
    )

@login_required
def shopper_dashboard(request):

    jobs = Assignment.objects.filter(
        shopper=request.user
    )

    return render(
        request,
        "core/shopper_dashboard.html",
        {"jobs": jobs}
    )