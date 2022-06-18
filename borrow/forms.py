from django import forms

from book.models import Book
from borrow.models import Borrow, Parametre
from reader.models import Reader

class Parametre_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Parametre_form, self).__init__(*args, **kwargs)
        self.fields['type'].label = "Type "
    class Meta:
        model=Parametre
        fields=['type','modalilte','valeur']
class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['date_borrow', 'expired_date_borrow']
    date_borrow = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),label="Date d'emprunt")
    expired_date_borrow = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}),label="Date d'expiration")


class RetourForm(forms.Form):
    idReader = forms.IntegerField(label='ID du lecteur : ')
