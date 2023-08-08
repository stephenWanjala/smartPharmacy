from django import forms

from pharmacy.models import Category, Medicine


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
