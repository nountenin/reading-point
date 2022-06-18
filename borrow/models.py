import types

from django.db import models
from book.models import Book, ReadPoint
from reader.models import Reader


# Create your models here.

class Borrow(models.Model):
    objects = None
    date_borrow = models.DateField()
    expired_date_borrow = models.DateField()
    return_date_borrow = models.DateField(blank=True, null=True, default=None)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return '{} {} {} {}'.format(
            self.pk,
            self.book.title_book,
            self.reader.first_name,
            self.expired_date_borrow
        )


class Parametre(models.Model):
    __types = [
        ('ancien', 'ancien'),
        ('frequence', 'frequence')
    ]
    readPoint = models.ForeignKey(ReadPoint, models.CASCADE)
    type = models.CharField(choices=__types,default='ancien',max_length=10)
    modalilte = models.CharField(choices=[('7', 'semaine'), ('30', 'mois'), ('365', 'annee')],default='30',max_length=10)
    valeur = models.IntegerField(default=1)
