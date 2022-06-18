from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import date, datetime
from accounting.models import *
from book.forms import BookForm
from accounting.forms import Persone_form, Depense_form, Vente_form
from django.db.models import Sum


# Create your views here.

def accounting(request):
    context = {
        'tooltip': "Comptabilite - Tableau de bord"
    }
    return render(request, 'accounting/accounting_dashboard.html', context)


def accounting_dashboard(request):
    return render(request, 'accounting/accounting_dashboard.html')


def depense_today(request):
    today = date.today()
    dp_today = Depense.objects.filter(created_at__day=today.day)
    print(dp_today)
    return render(request, 'accounting/depense.html', {'dp_today': dp_today})


def depense(request):
    compte = None
    cmpt = 0
    try:
        compte = Compte.objects.last()
        cmpt = compte.solde_compte
    except:
        pass
    depense = Depense.objects.all()
    today = date.today()
    dp_today = Depense.objects.filter(created_at__day=today.day)
    sum_today = dp_today.aggregate(Sum('total_depense')).get('total_depense__sum')
    dp_month = Depense.objects.filter(created_at__month=today.month)
    if request.method == "POST":
        depense_form = Depense_form(request.POST)
        if depense_form.is_valid():
            val = depense_form.save()
            new_solde = cmpt - val.total_depense
            new = Compte(solde_compte=new_solde)
            new.save()
            return redirect("depense")
        else:
            return render(request, 'accounting/depense.html', context={
                'depense': depense,
                'depense_form': depense_form,
                'dp_today': dp_today,
                'dp_month': dp_month
            })
    else:
        depense_form = Depense_form()
        return render(request, 'accounting/depense.html', {
            'depense': depense,
            'depense_form': depense_form,
            'dp_today': dp_today,
            'dp_month': dp_month,
            'sum_today': sum_today
        })


def recherche_depense(request):
    depense = Depense.objects.all()
    depense_form = Depense_form()
    return render(request, 'accounting/recherche_depense.html', {
        'depense': depense,
        'depense_form': depense_form
    })


def payer(request, id):
    compte = Compte.objects.last()
    cmpt = compte.solde_compte
    person = Personel.objects.get(id=id)
    person_payer = Payer.objects.create(personnel=person, etat_payer=True, solde_paiement=person.salaire_personnel)
    new_solde = cmpt - person.salaire_personnel
    new = Compte(solde_compte=new_solde)
    new.save()
    person_payer.save()

    # anc = ancien.solde_paiement
    # anc += person.salaire_personnel
    return redirect('personel')


def personel(request):
    compte = None
    cmpt = 0
    try:
        compte = Compte.objects.last()
        cmpt = compte.solde_compte
    except:
        pass
    person = Personel.objects.all()
    if request.method == "POST":
        person_form = Persone_form(request.POST)
        if person_form.is_valid():
            # val = person_form.save()
            # new_solde = cmpt - val.salaire_personnel
            # new = Compte(solde_compte=new_solde)
            person_form.save()
            return redirect("personel")
        else:
            return render(request, 'accounting/personel.html', context={
                'personel': person,
                'person_form': person_form
            })
    else:
        person_form = Persone_form()
        return render(request, 'accounting/personel.html', {
            'person': person,
            'person_form': person_form
        })


def tresorerie(request):
    # annee = Depense.objects.get(created_at__year=recherche_annee)
    today = date.today()
    num_moi = today.month
    # total_m = today.month
    # total_mois = dp_today.aggregate(Sum('total_depense')).get('total_depense__sum')
    res = Depense.objects.filter(created_at__month__lte=4).aggregate(Sum('total_depense')).get('total_depense__sum')
    print("######*** les mois inferieur", res)
    mois = {
        'janv': Depense.objects.filter(created_at__month=1).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'fev': Depense.objects.filter(created_at__month=2).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'mars': Depense.objects.filter(created_at__month=3).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'avril': Depense.objects.filter(created_at__month=4).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'mai': Depense.objects.filter(created_at__month=5).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'juin': Depense.objects.filter(created_at__month=6).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'juill': Depense.objects.filter(created_at__month=7).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'aout': Depense.objects.filter(created_at__month=8).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'sept': Depense.objects.filter(created_at__month=9).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'oct': Depense.objects.filter(created_at__month=10).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'nov': Depense.objects.filter(created_at__month=11).aggregate(Sum('total_depense')).get('total_depense__sum'),
        'dec': Depense.objects.filter(created_at__month=12).aggregate(Sum('total_depense')).get('total_depense__sum'),
    }

    return render(request, 'accounting/tresorerie.html', context={
        'mois': mois,
        'compte_mois': res
    })


def vente(request):
    return render(request, 'accounting/vente.html', context={})

# def vente(request):
#     if request.method == "POST":
#         form = AchatForm(request.POST, request.FILES)
#         achar = Achat.objects.filter(isbn_book=request.POST['isbn_book']).filter(category=request.POST['category'])
#         if achat:
#             context = {
#                 'tooltip': 'Livres',
#                 'form': form,
#                 'message': 'Ce livre existe dejà dans cette categorie'
#             }
#             return render(request, 'accounting/vente.html', context)
#         else:
#             if form.is_valid():
#                 form.save()
#                 return redirect('vente')
#             return render(request, 'accounting/vente.html', {'form': form})
#     else:
#         form = AchatForm()
#         context = {
#             'tooltip': 'Achats',
#             'form': form
#         }
#         return render(request, 'accounting/vente.html', context)


def bulletin_paie(request, id):
    person_form = Persone_form()
    bulletin_person = Payer.objects.filter(personnel_id=id)
    print("############************",bulletin_person)
    context = {
        'bulletin_person': bulletin_person,
        'person_form': person_form
    }
    return  render(request,'accounting/personel.html',context)
