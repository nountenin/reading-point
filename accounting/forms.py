from crispy_forms.helper import FormHelper
from django import forms
from book.forms import BookForm
from .models import *


# class TimesheetItemForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # init is used for other fields initialization and crispy forms
#
#     class Meta:
#         model = TimesheetItem
#         fields = ['date', 'description']
#
#         widgets = {
#             'date': forms.DateInput(
#                 format=('%Y-%m-%d'),
#                 attrs={'class': 'form-control',
#                        'placeholder': 'Select a date',
#                        'type': 'date'
#                        }),
#         }


class Depense_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Depense_form, self).__init__(*args, **kwargs)
        self.fields['libelle_depense'].label = "Libelle"
        self.fields['description_depense'].label = "Description"
        self.fields['prix_ht_depense'].label = "Prix"
        self.fields['quantite_depense'].label = "Quantite"
        self.fields['total_depense'].label = "Total"

    class Meta:
        model = Depense
        fields = [
            'libelle_depense',
            'description_depense',
            'prix_ht_depense',
            'quantite_depense',
            'total_depense'
        ]


class Vente_form(forms.ModelForm):
    def __str__(self, *args, **kwargs):
        super(Vente_form, self).__str__(*args, **kwargs)
        self.fields['article_vente'].label = "Article"
        self.fields['description_vente'].label = "Description"
        self.fields['prix_vente'].label = "Prix de vente"
        self.fields['total_vente'].label = "Total"

    class Meta:
        model = Ventes
        fields = [
            'article_vente',
            'description_vente',
            'prix_vente',
            'total_vente'
        ]


class Persone_form(forms.ModelForm):
    def __str__(self, *args, **kwargs):
        super(Persone_form, self).__str__(*args, **kwargs)
        self.fields['nom_personnel'].label = nom_personnel
        self.fields['prenom_personnel'].label = prenom_personnel
        self.fields['fonction_personnel'].label = prenom_personnel

    class Meta:
        model = Personel
        fields = [
            'nom_personnel',
            'prenom_personnel',
            'fonction_personnel'
        ]