# Generated by Django 4.2.20 on 2025-04-15 13:33

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('number_of_guests', models.PositiveIntegerField()),
                ('code', models.CharField(editable=False, max_length=8, null=True, unique=True)),
                ('reservation_link', models.URLField(blank=True, null=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='bookings.apartment')),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=1)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('date_of_birth', models.DateField(blank=True)),
                ('identity_number', models.CharField(max_length=100)),
                ('document_type', models.CharField(choices=[('ID', 'Identity Card'), ('PP', 'Passport'), ('DL', 'Driving License')], default='ID', max_length=2)),
                ('document_number', models.CharField(max_length=100)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.reservation')),
            ],
        ),
    ]
