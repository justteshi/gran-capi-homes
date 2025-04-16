from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='add_error_class')
def add_error_class(field, errors):
    # Check if there are any errors
    if errors:
        # Add the 'is-invalid' class to the widget's existing class
        classes = field.widget.attrs.get('class', '').split()
        if 'form-control' not in classes:
            classes.append('form-control')  # Make sure form-control is included
        if 'is-invalid' not in classes:
            classes.append('is-invalid')  # Add the is-invalid class if errors exist
        field.field.widget.attrs['class'] = ' '.join(classes)

    return field

