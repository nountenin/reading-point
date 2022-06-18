from django.urls import path
from .views import *

urlpatterns = [
    path('accounting/', accounting_dashboard, name="accounting_dashboard"),
    path('depense/',depense, name="depense"),
    path('recherche_depense/',recherche_depense, name="recherche_depense"),
    path('payer/<int:id>',payer, name="payer"),
    path('personel/',personel,name="personel"),
    path('tresorerie/',tresorerie,name="tresorerie"),
    path('vente/',vente,name="vente"),
    path('bulletin_paie/<int:id>',bulletin_paie,name="bulletin_paie")
]