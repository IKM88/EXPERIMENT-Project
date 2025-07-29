from django import forms
from .models import ContactInquiry, Testimonial


class ContactForm(forms.ModelForm):
    """
    Form for contact inquiries with professional styling.
    Provides validation and user-friendly field presentation.
    """
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'company_name', 'inquiry_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@company.com',
                'required': True
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Company Name (Optional)'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Please describe your inquiry in detail...',
                'required': True
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'company_name': 'Company Name',
            'inquiry_type': 'Type of Inquiry',
            'message': 'Message',
        }


class TestimonialForm(forms.ModelForm):
    """
    Form for testimonial submissions with rating system.
    Submitted testimonials require admin approval before display.
    """
    class Meta:
        model = Testimonial
        fields = ['name', 'company', 'rating', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Company (Optional)'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with Al-Solution...',
                'required': True
            }),
        }
        labels = {
            'name': 'Your Name',
            'company': 'Company',
            'rating': 'Rating',
            'comment': 'Your Testimonial',
        }