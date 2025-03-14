from django import forms
from apps.solicitations.models.perdiem_models import PerDiemRequest, PerDiemRequestItem

class PerDiemRequestForm(forms.ModelForm):
    class Meta:
        model = PerDiemRequest
        fields = [
            "solicitation",
            "vehicles",
            "start_date",
            "end_date",
            "days",
            "persons",
            "details",
            "total_expense",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "days": forms.NumberInput(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "vehicles": forms.SelectMultiple(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "persons": forms.SelectMultiple(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "details": forms.Textarea(attrs={"rows": 3, "class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "total_expense": forms.NumberInput(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
        }


class PerDiemRequestItemForm(forms.ModelForm):
    class Meta:
        model = PerDiemRequestItem
        fields = [
            "request_service",
            "item",
            "price",
            "amount",
            "currency",
            "description",
            "total_price",
        ]
        widgets = {
            "item": forms.Select(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "price": forms.NumberInput(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "amount": forms.NumberInput(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "currency": forms.Select(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "description": forms.TextInput(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500"}),
            "total_price": forms.NumberInput(attrs={"class": "w-full px-4 py-2 border rounded-md focus:ring-blue-500 focus:border-blue-500", "readonly": "readonly"}),
        }

    def clean_total_price(self):
        price = self.cleaned_data.get("price", 0)
        amount = self.cleaned_data.get("amount", 1)
        return price * amount