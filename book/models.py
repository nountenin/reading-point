from datetime import datetime

from django import forms
from django.db import models
from django.db.models import Avg


# from web_site_front.models import Commentaires
# from reader.models import Reader


class Author(models.Model):
    first_name_author = models.CharField(max_length=50)
    last_name_author = models.CharField(max_length=50)
    biography_author = models.CharField(max_length=255, blank=True, null=True)
    nationality_author = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{} {}".format(
            self.first_name_author,
            self.last_name_author
        )


# Table Point de lecture
class ReadPoint(models.Model):
    name_readpoint = models.CharField(max_length=50)
    commune_readpoint = models.CharField(max_length=50)
    quartier_readpoint = models.CharField(max_length=50)
    address_readpoint = models.CharField(max_length=50)
    contact1_readpoint = models.CharField(max_length=50)
    contact2_readpoint = models.CharField(max_length=50)
    email_readpoint = models.EmailField(max_length=50)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "Nom: {name} Commune: {commune} Quartier: {quartier}".format(
            name=self.name_readpoint,
            commune=self.commune_readpoint,
            quartier=self.quartier_readpoint
        )


class Rayon(models.Model):
    name_rayon = models.CharField(max_length=50)
    readpoint = models.ForeignKey(ReadPoint, on_delete=models.CASCADE)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return " {rayon}".format(
            rayon=self.name_rayon
        )


# Create your models here.
class Category(models.Model):
    name_category = models.CharField(max_length=30)
    rayon = models.ForeignKey(Rayon, on_delete=models.CASCADE)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{}".format(
            self.name_category
        )


class Book(models.Model):
    isbn_book = models.CharField(max_length=30)
    title_book = models.CharField(max_length=30)
    number_copy_book = models.IntegerField()
    publication_date_book = models.DateField()
    file_book = models.FileField(upload_to='book_electroniques', blank=True, null=True)
    img1_book = models.ImageField(upload_to='couverture')
    img2_book = models.ImageField(upload_to='couverture')
    resume_book = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    edition_house = models.CharField(max_length=30)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    notes = models.IntegerField(null=True)

    class Meta:
        ordering = ['notes']

    def __str__(self):
        return "Titre: {} Auteur: {} {} {}".format(
            self.title_book,
            self.author.first_name_author,
            self.author.last_name_author,
            self.isbn_book
        )

    def nouveau(self):
        return (datetime.now().date() - self.created_at.date()).days < 50

    def note(self):
        return Commentaires.objects.filter(book=self.pk).aggregate(Avg('note'))


class Commentaires(models.Model):
    lecteur = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    commentaire = models.TextField()
    note = models.IntegerField()
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.note} {self.book}"


class Movement(models.Model):
    type = [
        ('', "Sélectionnez un type de mouvement"),
        (1, "Stock Initial"),
        (2, "Approvisionnement"),
        (3, "Emprunt"),
        (4, "Retour"),
        (5, "Transfert")
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    motif = models.TextField()
    type = models.SmallIntegerField(choices=type)
    quantite = models.IntegerField()
    date_movement = models.DateField(auto_now_add=True)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return '{} {} {}'.format(
            self.book.isbn_book,
            self.type,
            self.motif
        )


class Transfert(models.Model):
    pointlectureEmetteur = models.IntegerField()
    pointlectureDestinateur = models.IntegerField()
    dateTransfert = models.DateTimeField(auto_now_add=True)
    desciption = models.TextField(null=True)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.pk} {self.pointlectureEmetteur} {self.pointlectureDestinateur} {self.dateTransfert} {self.desciption}"


class Item_transfert(models.Model):
    livre = models.ForeignKey(Book, on_delete=models.CASCADE)
    transfert = models.ForeignKey(Transfert, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.pk} {self.livre} {self.transfert} {self.quantite}"
