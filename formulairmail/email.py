from django import forms


class mail(forms.Form):
    mail = forms.EmailField(label="Email:", max_length=100)
