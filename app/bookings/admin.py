from django.contrib import admin
from .models import Apartment, Reservation, Guest, Policy
from django.utils.html import format_html
from django.urls import reverse

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 0
    can_delete = False
    show_change_link = False  # We're adding our own link
    readonly_fields = ("code", "check_in", "check_out", "number_of_guests", "edit_link")
    fields = ("code", "check_in", "check_out", "number_of_guests", "edit_link")

    def has_add_permission(self, request, obj=None):
        return False

    def edit_link(self, obj):
        if obj.pk:
            url = reverse("admin:bookings_reservation_change", args=[obj.pk])
            return format_html('<a href="{}" class="btn btn-primary">Edit</a>', url)
        return "-"
    edit_link.short_description = "Edit"

class GuestInline(admin.TabularInline):  # Or use StackedInline for a more detailed layout
    model = Guest
    extra = 0  # Do not show empty extra fields
    readonly_fields = ['first_name', 'middle_name', 'last_name', 'sex', 'country', 'date_of_birth', 'identity_number', 'document_type', 'document_number']
    can_delete = False  # Optional: prevent deletion from admin
    show_change_link = True  # Optional: make each row clickable

class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ReservationInline]


class ReservationAdmin(admin.ModelAdmin):
    # Display the 'reservation_link' as a clickable URL
    list_display = ("code", "apartment", "check_in", "check_out", "number_of_guests", "reservation_link_html")
    inlines = [GuestInline]
    # Custom method to format 'reservation_link' as clickable HTML
    def reservation_link_html(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.reservation_link,
            'Check-in Link'
        )

    reservation_link_html.short_description = "Reservation Link"

    list_filter = ("apartment", "check_in", "check_out")
    search_fields = ("code", "apartment__title")
    readonly_fields = ('code', 'reservation_link', 'terms_agreed')
    fields = ('apartment', 'check_in', 'check_out', 'number_of_guests', 'code', 'reservation_link', 'terms_agreed')



class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'reservation')
    search_fields = ('first_name', 'last_name')
    list_filter = ('reservation', 'first_name')


class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    readonly_fields = ('preview',)

    def preview(self, obj):
        return format_html(obj.content)
    preview.short_description = "Preview"


admin.site.register(Guest, GuestAdmin)
admin.site.register(Policy, PolicyAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Reservation, ReservationAdmin)
