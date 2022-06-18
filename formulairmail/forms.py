from crispy_forms.helper import FormHelper
from django import forms

from formulairmail.models import Email


class Email_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Email_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Email
        fields = [
            'email_exp',
            'message',
            'object'
        ]

class mail(forms.Form):
    mail = forms.EmailField(label="Email:", max_length=100)


