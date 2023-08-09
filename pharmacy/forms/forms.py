from datetime import timedelta

from django import forms
from django.utils.datetime_safe import date

from pharmacy.models import Category, Medicine, Purchase, Sale


class MedicineCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to the form fields' widgets
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['medicine', 'quantity_purchased', 'purchase_amount', 'purchase_date', 'expiry_date', 'supplier']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'quantity_purchased': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today()
        self.fields['purchase_date'].widget.attrs['max'] = today
        self.fields['expiry_date'].widget.attrs['min'] = today + timedelta(days=8)


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['medicine', 'quantity_sold', ]
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'quantity_sold': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity-sold'}),
            # 'selling_price': forms.NumberInput(
            #     attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'selling-price', 'disabled': 'disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter medicines that are not out of stock
        self.fields['medicine'].queryset = Medicine.objects.filter(stock__quantity__gt=0)
