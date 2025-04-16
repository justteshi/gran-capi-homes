from django import forms
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from django.utils.safestring import mark_safe
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
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

            field.widget.attrs['id'] = f'id_{field_name}'
            field.required = True

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

class TermsAgreementForm(forms.Form):
    terms_agreed = forms.BooleanField(
        required=True,
        label=mark_safe(
            "I agree to the <a href='#' data-bs-toggle='modal' data-bs-target='#termsModal'>Terms and Conditions and Privacy Policy</a>"),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox'})
    )