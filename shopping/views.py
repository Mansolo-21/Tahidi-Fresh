from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ShoppingRequestForm,AssignmentForm
from .models import ShoppingRequest,Assignment,Activity

@login_required
def create_request(request):
    form = ShoppingRequestForm()
    if request.method == "POST":
        form=ShoppingRequestForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            shopping_request= form.save(commit=False)
            shopping_request.customer = request.user
            shopping_request.save()
            Activity.objects.create(
                request=shopping_request,
                description="Request Created"
            )
            return redirect("request_list")
    return render(request,"shopping/create_request.html",{"form":form})

@login_required
def request_list(request):

    requests = ShoppingRequest.objects.filter(
            customer=request.user
    ).order_by("-created_at")

    return render(
    request,
    "shopping/request_list.html",
    {
        "requests": requests
    }
)

def assign_workers(request, pk):
    shopping_request = get_object_or_404(
        ShoppingRequest,pk=pk
    )

    assignment, created = (
        Assignment.objects.get_or_create(
            request=shopping_request
        )
    )

    if request.method =="POST":
        form=AssignmentForm(
            request.POST,
            instance=assignment
        )
        if form.is_valid():
            form.save()
            
            assignment= form.instance
            if assignment.shopper:
                Activity.objects.create(
                    request=shopping_request,
                    description=f"Shopper Assigned:{assignment.shopper.username}"
                )
            if assignment.rider:
                Activity.objects.create(
                    request=shopping_request,
                    description=f"Rider Assigned:{assignment.rider.username}"
                )
            shopping_request.status ="assigned"
            shopping_request.save()

            return redirect(
                "request_detail",
                pk=pk
            )
    else:
        form=AssignmentForm(
            instance=assignment
        )
    return render(request,"shopping/asssign_workers.html",{"form":form,"request_obj":shopping_request})

def request_detail(request,pk):
    shopping_request = get_object_or_404(
        ShoppingRequest,
        pk=pk
    )
    assignment = Assignment.objects.filter(
        request=shopping_request).first()
    
    activities=shopping_request.activities.all().order_by("created_at")
    
    return render(request,"shopping/request_detail.html",{
            "shopping_request":shopping_request,
            "assignment":assignment,
            "activities":activities
        })

def update_status(request,pk,status):
    shopping_request = get_object_or_404(
        ShoppingRequest,pk=pk
    )
    shopping_request.status=status
    status_messages={
        "shopping":"Shopping Started",
        "payment":"Awaiting Payment",
        "ready":"Ready For Delivery",
        "delivery":"Delivery",
        "completed":"Completed",
    }
    shopping_request.save()
    Activity.objects.create(
        request=shopping_request,
        description=status_messages.get(
            status,status
        )
    )

    return redirect("request_detail",pk=pk)

@login_required
def shopper_dashboard(request):

    assignments=Assignment.objects.filter(
        shopper=request.user
    )
    return render(request,"shopping/shopper_dashboard.html",{"assignments":assignments})

