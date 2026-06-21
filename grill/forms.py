from django import forms
from django.forms import ModelForm
from .models import MenuItem
from .models import FoodAssignment
from accounts.models import User

class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "rows":3
            }
        )
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "rows":3
            }
        )
    )

class FoodAssignmentForm(forms.ModelForm):

    class Meta:
        model = FoodAssignment
        fields = [
            "rider"
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["rider"].queryset = (
            User.objects.filter(
                can_deliver=True
            )
        )


class MenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = [
            "name",
            "price",
            "description",
            "image",
            "available"
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "available": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }