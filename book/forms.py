from crispy_forms.helper import FormHelper
from django import forms
from book.models import ReadPoint, Rayon
from .models import Book, Category, Author, Movement

id_user_readpoint = 0


class ReadPoint_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReadPoint_form, self).__init__(*args, **kwargs)
        self.fields['name_readpoint'].label = "Nom "
        self.fields['commune_readpoint'].label = "Commune "
        self.fields['quartier_readpoint'].label = "Quartier "
        self.fields['address_readpoint'].label = "Adresse "
        self.fields['contact1_readpoint'].label = "Contact 1 "
        self.fields['contact2_readpoint'].label = "Contact 2 "
        self.fields['email_readpoint'].label = "Email "

    class Meta:
        model = ReadPoint
        fields = [
            'name_readpoint',
            'commune_readpoint',
            'quartier_readpoint',
            'address_readpoint',
            'contact1_readpoint',
            'contact2_readpoint',
            'email_readpoint',
        ]


class Rayon_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Rayon_form, self).__init__(*args, **kwargs)
        self.fields['name_rayon'].label = "Nom "
        self.fields['readpoint'].label = "Point de lecture "

    class Meta:
        model = Rayon
        fields = [
            'name_rayon',
            'readpoint'
        ]


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Book
        fields = [
            'isbn_book',
            'title_book',
            'number_copy_book',
            'publication_date_book',
            'file_book',
            'resume_book',
            'category',
            'img1_book',
            'img2_book',
            'author',
            'edition_house'
        ]

    publication_date_book = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    category = forms.ModelChoiceField(queryset=Category.objects.filter(status=1),
                                      empty_label="Sélectionnez une catégorie")
    author = forms.ModelChoiceField(queryset=Author.objects.filter(status=1), empty_label="Sélectionnez un auteur")


class Category_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Category_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Category
        fields = [
            'name_category'
        ]


class Author_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Author_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Author
        fields = [
            'first_name_author',
            'last_name_author',
            'biography_author',
            'nationality_author'
        ]


class Movement_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Movement_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Movement
        fields = [
            'book',
            'quantite',
            'motif',
            'type'
        ]

    book = forms.ModelChoiceField(queryset=Book.objects.filter(status=1), empty_label="Sélectionnez un livre")


class Movement_form_filtre(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Movement_form_filtre, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    type = forms.ChoiceField(choices=[
        ('', "Sélectionnez un type"),
        (1, "Stock Initial"),
        (2, "Approvisionnement"),
        (3, "Emprunt"),
        (4, "Retour"),
        (5, "Transfert")
    ], required=False)
