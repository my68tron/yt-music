from django import forms
from django.core import validators

def check_for_z(value):
    if value[0] != ('z' and 'Z'):
        raise forms.ValidationError("NAME NEEDS TO START WITH Z")

class SearchForm(forms.Form):
    """SearchForm definition."""

    name = forms.CharField(validators=[check_for_z])
    email = forms.EmailField()
    verify_email = forms.EmailField(label='Retype Email')
    textarea = forms.CharField(widget=forms.Textarea)
    botcatcher = forms.CharField(required=False,
                                 widget=forms.HiddenInput,
                                 validators=[validators.MaxLengthValidator(0)])

    def clean(self):
        all_clean_data = super().clean()
        email = all_clean_data['email']
        verify_email = all_clean_data['verify_email']

        if email != verify_email:
            raise forms.ValidationError("Email does not match")