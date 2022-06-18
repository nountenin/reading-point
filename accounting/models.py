from django.db import models
from book.models import Book


# Create your models here.

# class TimesheetItem(models.Model):
#     date = models.DateField()
#     description = models.CharField(max_length=100)


class Compte(models.Model):
    solde_compte = models.IntegerField(default=0)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{solde_compte}".format(
            solde_compte=self.solde_compte
        )

    def add_solde(self, val):
        self.solde_compte += val
        print("******** Nouveau solde **  :  ", self.solde_compte)


libelles_depenses = [
    ('Achat de fourniture', 'Achat de fourniture'),
    ('Achat de meuble', 'Achat de meuble'),
    ('Entretien du bureau', 'Entretien du bureau'),
    ('Reparation', 'Reparation'),
    ('Autres', 'Autres')
]


class Depense(models.Model):
    libelle_depense = models.CharField(max_length=100, choices=libelles_depenses)
    description_depense = models.CharField(max_length=255, null=True, blank=True)
    prix_ht_depense = models.IntegerField()
    quantite_depense = models.IntegerField(default=0)
    total_depense = models.IntegerField(default=0)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{libelle_depense} {description_depense} {prix_ht_depense} {quantite_depense} {total_depense} {created_at}".format(
            libelle_depense=self.libelle_depense,
            description_depense=self.description_depense,
            prix_ht_depense=self.prix_ht_depense,
            quantite_depense=self.quantite_depense,
            total_depense=self.total_depense,
            created_at=self.created_at
        )


class Personel(models.Model):
    nom_personnel = models.CharField(max_length=20)
    prenom_personnel = models.CharField(max_length=20)
    salaire_personnel = models.IntegerField(default=50000)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    fonction_personnel = models.CharField(max_length=30)

    def __str__(self):
        return "{nom_personnel} {prenom_personnel} {fonction_personnel} {salaire_personnel}".format(
            nom_personnel=self.nom_personnel,
            prenom_personnel=self.prenom_personnel,
            fonction_personnel=self.fonction_personnel,
            salaire_personnel=self.salaire_personnel
        )

class Payer(models.Model):
    personnel = models.ForeignKey(Personel, on_delete=models.DO_NOTHING)
    solde_paiement = models.IntegerField()
    etat_payer = models.BooleanField(default=False)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{personnel} {solde_paiement} {etat_payer}".format(
            personnel = self.personnel,
            solde_paiement = self.solde_paiement,
            etat_payer = self.etat_payer
        )


class Ventes(models.Model):
    article_vente = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    description_vente = models.CharField(max_length=255, blank=True)
    prix_vente = models.IntegerField()
    total_vente = models.IntegerField(default=0)
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{article_vente} {description_vente} {prix_vente} {total_vente}".format(
            article_vente=self.article_vente,
            description_vente=self.description_vente,
            prix_vente=self.prix_vente,
            total_vente=self.total_vente
        )

class Achat(Book):
    fournisseur = models.CharField(max_length=50)
    prix_achat = models.IntegerField()

    def __str__(self):
        return "{fournisseur} {prix_achat} {title_book} {author} {edition_house}".format(
            fournisseur=self.fournisseur,
            prix_achat=self.prix_achat,
            title_book=self.title_book,
            author =self.author,
            edition_house=self.edition_house
        )