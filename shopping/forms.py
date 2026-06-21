from django import forms
from .models import ShoppingRequest
from .models import Assignment
from accounts.models import User

class ShoppingRequestForm(forms.ModelForm):
    class Meta:
        model = ShoppingRequest
        fields =(
            "supermarket",
            "delivery_address",
            "shopping_list_text",
            "shopping_list",
            "notes",
        )
        widgets={"supermarket":forms.Select(
                        attrs={"class":"form-select"}
                    ),
                    "delivery_addresss":forms.Textarea(
                        attrs={
                            "class":"form-control",
                            "rows":3
                        }
                    ),
                    "shopping_list_text":forms.Textarea(
                        attrs={
                            "class":"form-control",
                            "rows":6,
                            "placeholder":"Enter your shopping list here"
                        }
                    ),
                    "shopping_list":forms.FileInput(
                        attrs={"class":"form-control"}
                    ),
                    "notes":forms.Textarea(
                        attrs={
                            "class":"form-control",
                            "rows":4
                        }
                    ),
                }
        
def clean(self):
    cleaned_data = super().clean()
    shopping_list_text = cleaned_data.get(
        "shopping_list_text"
    )
    shopping_list = cleaned_data.get(
        "shopping_list"
    )
    if not shopping_list_text and not shopping_list:
        raise forms.ValidationError(
            "Please upload a shopping list or type one."
        )
    return cleaned_data


class AssignmentForm(forms.ModelForm):
    class Meta:
        model=Assignment
        fields=[
            "shopper",
            "rider",
        ]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["shopper"].queryset=(
            User.objects.filter(
                can_shop=True
            )
        )

        self.fields["rider"].queryset=(
            User.objects.filter(
                can_deliver=True
            )
        )