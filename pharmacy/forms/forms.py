from django import forms

from pharmacy.models import Category, Medicine, Purchase, Sale, Stock


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
            # Set widget for expiration_date field
        self.fields['expiration_date'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['medicine', 'quantity_purchased', 'purchase_amount', 'purchase_date', 'supplier']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'quantity_purchased': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['medicine', 'quantity_sold', 'selling_price', 'customer_name']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'quantity_sold': forms.NumberInput(attrs={'class': 'form-control'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


