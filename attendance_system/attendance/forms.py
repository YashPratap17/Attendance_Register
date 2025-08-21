from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Describe the problem you faced today..."
            })
        }
