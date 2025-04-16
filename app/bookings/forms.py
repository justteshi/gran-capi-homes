from django import forms
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from .models import Guest

class GuestInfoForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            'first_name', 'middle_name', 'last_name', 'sex', 'country',
            'date_of_birth', 'identity_number', 'document_type', 'document_number'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'sex': forms.Select(),
            'document_type': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Use form-select for <select> fields, form-control for others
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.widget.attrs['id'] = f'id_{field_name}'
            field.required = True

            # Add 'is-invalid' class if there are any errors
            if field.errors:
                classes = field.widget.attrs.get('class', '').split()
                if 'form-control' not in classes:
                    classes.append('form-control')  # Ensure form-control is present
                if 'is-invalid' not in classes:
                    classes.append('is-invalid')  # Add is-invalid if errors
                field.widget.attrs['class'] = ' '.join(classes)

    # Optional: custom validation example
    def clean_identity_number(self):
        identity_number = self.cleaned_data.get('identity_number')
        if not identity_number.isalnum():
            raise forms.ValidationError("Identity number must be alphanumeric.")
        return identity_number

    def clean_document_number(self):
        doc_number = self.cleaned_data.get('document_number')
        if len(doc_number) < 5:
            raise forms.ValidationError("Document number must be at least 5 characters.")
        return doc_number


    # Field-level validation for 'full_name'
    # def clean_full_name(self):
    #     full_name = self.cleaned_data.get('full_name')
    #
    #     # Ensure that full name is not empty
    #     if not full_name:
    #         raise ValidationError('Full name is required.')
    #
    #     # Optionally, you could add more validation for the name format, e.g., no numbers allowed
    #     if any(char.isdigit() for char in full_name):
    #         raise ValidationError('Full name should not contain numbers.')
    #
    #     return full_name
    #
    # # Field-level validation for 'email'
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #
    #     # Ensure that email is not empty (though this is checked by the EmailField)
    #     if not email:
    #         raise ValidationError('Email is required.')
    #
    #     # You can add additional custom checks if needed
    #     if email and '@' not in email:
    #         raise ValidationError('Please enter a valid email address.')
    #
    #     return email
