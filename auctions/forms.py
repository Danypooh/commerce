from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_price', 'image', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 3}),
            'starting_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter starting price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'starting_price': 'Starting Price ($)'
        }
