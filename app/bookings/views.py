from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation, Guest
from .forms import GuestInfoForm, TermsAgreementForm
from django.forms import formset_factory
from admin_interface.models import Theme


def guest_info_view(request, code):
    reservation = get_object_or_404(Reservation, code=code.upper())
    max_guests = reservation.number_of_guests  # Number of guests for this reservation
    theme = Theme.objects.filter(active=True).first()

    # Create a formset factory for the number of guests
    GuestFormSet = formset_factory(GuestInfoForm,
                                   extra=0)  # We will not use `extra` because we want exactly max_guests forms
    terms_form = TermsAgreementForm(request.POST or None)  # Initialize the terms form

    if request.method == 'POST':
        formset = GuestFormSet(request.POST)

        # Check if the formset is valid and that all forms in the formset are valid
        if formset.is_valid() and terms_form.is_valid():
            # Iterate through the valid formset and save the data
            for form in formset:
                guest_data = form.cleaned_data
                if guest_data:  # Only create Guest if the form has valid data
                    Guest.objects.create(
                        reservation=reservation,
                        first_name=guest_data['first_name'],
                        middle_name=guest_data['middle_name'],
                        last_name=guest_data['last_name'],
                        sex=guest_data['sex'],
                        country=guest_data['country'],
                        date_of_birth=guest_data['date_of_birth'],
                        identity_number=guest_data['identity_number'],
                        document_type=guest_data['document_type'],
                        document_number=guest_data['document_number']
                    )

            # After saving guest data, save the terms agreement to the reservation
            reservation.terms_agreed = terms_form.cleaned_data['terms_agreed']
            reservation.save()

            # Redirect to success page
            return redirect('guest_info_success', code=reservation.code)

        else:
            # If the formset or terms form is invalid, pass the errors back to the template
            return render(request, 'bookings/guest_info.html', {
                'reservation': reservation,
                'formset': formset,
                'terms_form': terms_form,  # Pass the terms form as well for re-rendering
                'theme': theme,
            })

    else:
        # Create a new formset instance with the correct number of forms based on the number of guests
        formset = GuestFormSet(initial=[{}] * max_guests)  # This creates empty forms for all guests

    return render(request, 'bookings/guest_info.html', {
        'reservation': reservation,
        'formset': formset,
        'terms_form': terms_form,  # Pass the terms form to the template
        'theme': theme,
    })

def guest_info_success_view(request, code):
    reservation = get_object_or_404(Reservation, code=code.upper())
    return render(request, 'bookings/guest_info_success.html', {'reservation': reservation})

def home_view(request):
    theme = Theme.objects.filter(active=True).first()
    return render(request, 'home.html', {'theme': theme})

def check_reservation(request):
    code = request.GET.get('code', '').strip()
    theme = Theme.objects.filter(active=True).first()

    try:
        reservation = Reservation.objects.get(code=code)
        return redirect(reservation.get_absolute_url())
    except Reservation.DoesNotExist:
        return render(request, 'home.html', {'error': 'Reservation code not found.', 'theme': theme})

