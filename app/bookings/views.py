from django.shortcuts import render, get_object_or_404, redirect
from .models import Reservation, Guest
from .forms import GuestInfoForm
from django.forms import formset_factory

def guest_info_view(request, code):
    reservation = get_object_or_404(Reservation, code=code.upper())
    max_guests = reservation.number_of_guests  # Number of guests for this reservation

    # Create a formset factory for the number of guests
    GuestFormSet = formset_factory(GuestInfoForm, extra=0)  # We will not use `extra` because we want exactly max_guests forms

    if request.method == 'POST':
        formset = GuestFormSet(request.POST)

        # Check if the formset is valid and that all forms in the formset are valid
        if formset.is_valid():
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
            return redirect('guest_info_success', code=reservation.code)

        else:
            # If the formset is invalid, pass the errors back to the template
            return render(request, 'bookings/guest_info.html', {
                'reservation': reservation,
                'formset': formset,
            })

    else:
        # Create a new formset instance with the correct number of forms based on the number of guests
        formset = GuestFormSet(initial=[{}] * max_guests)  # This creates empty forms for all guests

    return render(request, 'bookings/guest_info.html', {
        'reservation': reservation,
        'formset': formset,
    })

def guest_info_success_view(request, code):
    reservation = get_object_or_404(Reservation, code=code.upper())
    return render(request, 'bookings/guest_info_success.html', {'reservation': reservation})


