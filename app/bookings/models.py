from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from tinymce.models import HTMLField
import uuid

class Apartment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Reservation(models.Model):
    apartment = models.ForeignKey('Apartment', on_delete=models.CASCADE, related_name='reservations')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField()
    code = models.CharField(max_length=8, unique=True, editable=False, null=True)
    reservation_link = models.URLField(max_length=200, null=True, blank=True)  # New field to store the link
    terms_agreed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = uuid.uuid4().hex[:8].upper()
        if not self.reservation_link:
            # Generate the reservation link using the unique code
            self.reservation_link = reverse('guest-info', kwargs={'code': self.code})
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} | {self.apartment.title} ({self.check_in.date()} - {self.check_out.date()})"

    def get_absolute_url(self):
        return reverse('guest-info', kwargs={'code': self.code})


class Guest(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    DOCUMENT_TYPE_CHOICES = [
        ('ID', 'Identity Card'),
        ('PP', 'Passport'),
        ('DL', 'Driving License'),
    ]

    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, related_name='guests')

    # Personal Information Fields
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)  # Middle name can be optional
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)  # M, F, O
    country = CountryField(blank=True)  # Using the CountryField provided by django-countries
    date_of_birth = models.DateField(blank=True)  # This will use a date picker in the form
    identity_number = models.CharField(max_length=100)

    # Document Information
    document_type = models.CharField(max_length=2, choices=DOCUMENT_TYPE_CHOICES)  # ID, PP, DL
    document_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.reservation.code})"

class Policy(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Policy'  # Singular form
        verbose_name_plural = 'Policies'
    def __str__(self):
        return self.title
