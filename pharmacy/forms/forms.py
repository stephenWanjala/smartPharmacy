from pharmacy.models import Category
from django import forms


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
