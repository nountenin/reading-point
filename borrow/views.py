from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

from book.forms import Movement_form
from book.models import Book
from borrow.forms import BorrowForm, RetourForm, Parametre_form
from borrow.models import Borrow, Parametre
# Create your views here.
from reader.models import Reader, Frequentation

expired_Borrow = []

@login_required(login_url='login')
def parametre(request):
    readpoint = Parametre.objects.get(readPoint=request.user.readpoint)
    form = Parametre_form(instance=readpoint)
    if request.method =="POST":
        form = Parametre_form(request.POST,instance=readpoint)
        if form.is_valid():
            form.save()
            messages.success(request,"Parametre modifier avec succès")
            return  redirect('parametre')
        else:
            return render(request,'borrow/parametre.html', {'form':form,'title':'Changement de Parametre'})
    else:
        return render(request,'borrow/parametre.html',{'form':form,'title':'Changement de Parametre'})


@login_required(login_url='login')
def add_borrows(request):
    noProblemen = True
    if request.user.has_perm('borrow.add_borrow'):
        parametre = Parametre.objects.get(readPoint=request.user.readpoint)
        if request.user.is_superuser:
            livre = Book.objects.filter(status=1)
            read = Reader.objects.filter(status=1).exclude(type_Reader=1)
        else:
            livre = Book.objects.filter(status=1).filter(category__rayon__readpoint_id=request.user.readpoint.pk)
            read = Reader.objects.filter(status=1).filter(readpoint=request.user.readpoint).exclude(type_Reader=1)
        if request.method == "POST":
            borrowForm = BorrowForm(request.POST)
            book_selected = int(request.POST['book']) if request.POST['book'] != '' else ''
            reader_selected = int(request.POST['reader']) if request.POST['reader'] != '' else ''
            if request.POST['book'] == '' or request.POST['reader'] == '':
                messages.error(request, "Donnée invalide")
                return render(request, 'borrow/addborrow.html',
                              {'form': borrowForm, 'book': livre, 'reader': read, 'tooltip': 'Ajout Emprunt',
                               'reader_selected': reader_selected,
                               'book_selected': book_selected,
                               'expired': expired_Borrow,
                               'notif': len(expired_Borrow)
                               })
            if borrowForm.is_valid():
                book = Book.objects.get(pk=int(request.POST['book']))
                if book.number_copy_book > 0:

                    if borrowForm.cleaned_data['date_borrow'] > date.today():
                        messages.error(request,
                                       "Erreur d'emprunt la date debut d'emprunt doit être inferieur ou egale a la date d'aujourd'hui veillez ressayer.",
                                       fail_silently=True
                                       )
                        noProblemen = False
                    if borrowForm.cleaned_data['expired_date_borrow'] < date.today():
                        messages.error(request,
                                       "Erreur d'emprunt la date fin d'emprunt  doit être superieur  a la date d'aujourd'hui veillez ressayer.",
                                       fail_silently=True
                                       )
                        noProblemen = False
                    if not noProblemen:
                        return render(request, 'borrow/addborrow.html',
                                      {'form': borrowForm, 'book': livre, 'reader': read, 'tooltip': 'Ajout Emprunt',
                                       'reader_selected': reader_selected,
                                       'book_selected': book_selected,
                                       'expired': expired_Borrow,
                                       'notif': len(expired_Borrow)
                                       })
                    else:
                        reade = Reader.objects.get(pk=request.POST['reader'])
                        books = Book.objects.get(pk=request.POST['book'])
                        noProblemen = True
                        if parametre.type == 'ancien':
                            if (reade.created_at.date() - datetime.datetime.today().date()).days < parametre.valeur * int(parametre.modalilte):
                                messages.error(request,f"Emprunt Impossible, Ce lecteur n'a pas une ancienete de {parametre.valeur} {parametre.get_modalilte_display()}")
                                noProblemen = False
                        elif parametre.type == 'frequence':
                            if parametre.modalilte == '7':
                                fequence = Frequentation.objects.filter(semaine=datetime.now().isocalendar()[1]).filter(
                                    lecteur=reade).filter(readpoint=request.user.readpoint).values('semaine').annotate(
                                    dcount=Count('lecteur')).order_by()
                                if fequence[0]['dcount'] < parametre.valeur:
                                    messages.error(request,
                                                   f"Emprunt Impossible, Ce lecteur n'est pas venu  {parametre.valeur} fois cette {parametre.get_modalilte_display()}")
                                    noProblemen = False
                            elif parametre.modalilte == '30':
                                fequence = Frequentation.objects.filter(mois=datetime.now().month).filter(
                                    lecteur=reade).filter(readpoint=request.user.readpoint).values('mois').annotate(
                                    dcount=Count('lecteur')).order_by()
                                if fequence[0]['dcount'] < parametre.valeur:
                                    messages.error(request,
                                                   f"Emprunt Impossible, Ce lecteur n'est pas venu  {parametre.valeur} fois ce {parametre.get_modalilte_display()}")
                                    noProblemen = False
                            elif parametre.modalilte == '365':
                                fequence = Frequentation.objects.filter(date_frequentation=datetime.now().year).filter(
                                    lecteur=reade).filter(readpoint=request.user.readpoint).values('date_frequentation').annotate(
                                    dcount=Count('lecteur')).order_by()
                                if fequence[0]['dcount'] < parametre.valeur:
                                    messages.error(request,
                                                   f"Emprunt Impossible, Ce lecteur n'est pas venu  {parametre.valeur} fois cette {parametre.get_modalilte_display()}")
                                    noProblemen = False
                        if not noProblemen:
                                 return render(request, 'borrow/addborrow.html',
                                              {'form': borrowForm, 'book': livre, 'reader': read,
                                               'tooltip': 'Ajout Emprunt',
                                               'reader_selected': reader_selected,
                                               'book_selected': book_selected,
                                               'expired': expired_Borrow,
                                               'notif': len(expired_Borrow)
                                               })
                        bo = borrowForm.save(commit=False)
                        bo.reader_id = int(reade.pk)
                        bo.book_id = int(books.pk)
                        bo.created_by = request.user.id
                        if not bo.save():
                            form = Movement_form({
                                'book': books,
                                'quantite': 1,
                                'motif': "Emprunt",
                                'type': 3
                            })
                            if form.is_valid():
                                formu = form.save(commit=False)
                                formu.created_by = request.user.id
                                if not formu.save():
                                    book.number_copy_book -= 1
                                    book.save()
                                    messages.success(request,
                                                     "Emprunter avec succés",
                                                     fail_silently=True
                                                     )
                                    return render(request, 'borrow/addborrow.html',
                                                  {'form': BorrowForm(), 'tooltip': 'Ajout Emprunt', 'book': livre,
                                                   'reader': read})
                                else:
                                    messages.error(request,
                                                   "Emprunt ajouté mais echec d'enregistrement de  mouvement",
                                                   fail_silently=True
                                                   )
                                    return render(request, 'borrow/addborrow.html',
                                                  {'form': form, 'tooltip': 'Ajout Emprunt', 'book': livre,
                                                   'reader': read,
                                                   'expired': expired_Borrow,
                                                   'notif': len(expired_Borrow)
                                                   })
                            else:
                                messages.error(request,
                                               "Emprunt ajouté mais echec d'enregistrement de  mouvement car les donnée sont invalid",
                                               fail_silently=True
                                               )
                        return render(request, 'borrow/addborrow.html',
                                      {'form': BorrowForm(), 'tooltip': 'Ajout Emprunt',
                                       'book': livre, 'reader': read,
                                       'reader_selected': reader_selected,
                                       'book_selected': book_selected,
                                       'expired': expired_Borrow,
                                       'notif': len(expired_Borrow)
                                       })

                else:
                    messages.info(request,
                                  "Ce livre est en rupture de stock veillez l'approvisionner .",
                                  fail_silently=True
                                  )
                    return render(request, 'borrow/addborrow.html',
                                  {'form': borrowForm, 'tooltip': 'Ajout Emprunt', 'book': livre, 'reader': read,
                                   'reader_selected': reader_selected,
                                   'book_selected': book_selected,
                                   'expired': expired_Borrow,
                                   'notif': len(expired_Borrow)
                                   })
            else:
                messages.error(request,
                               "Erreur d'emprunt verifier bien le formulaire.",
                               fail_silently=True
                               )
                return render(request, 'borrow/addborrow.html',
                              {
                                  'form': borrowForm,
                                  'tooltip': 'Ajout Emprunt',
                                  'book': livre,
                                  'reader': read,
                                  'reader_selected': reader_selected,
                                  'book_selected': book_selected,
                                  'expired': expired_Borrow,
                                  'notif': len(expired_Borrow)
                              })
        else:
            borrowForm = BorrowForm()
            context = {
                'tooltip': 'Ajout Emprunt',
                'form': borrowForm,
                'book': livre,
                'reader': read,
                'expired': expired_Borrow,
                'notif': len(expired_Borrow)

            }
            return render(request, 'borrow/addborrow.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def borrow(request):
    if request.user.has_perm('borrow.view_borrow'):
        if request.user.is_superuser:
            borrows = Borrow.objects.filter(status=1)
        else:
            borrows = Borrow.objects.filter(status=1).filter(book__category__rayon__readpoint=request.user.readpoint.pk)
        new_borrows = []
        for borrow in borrows:
            b = {
                'pk': borrow.pk,
                'date_borrow': borrow.date_borrow,
                'expired_date_borrow': borrow.expired_date_borrow,
                'return_date_borrow': borrow.return_date_borrow,
                'reader': borrow.reader,
                'book': borrow.book,
                'stat': borrow.expired_date_borrow > date.today(),
                'days': (borrow.expired_date_borrow - date.today()).days
            }
            new_borrows.append(b)
        context = {
            'tooltip': 'Liste des emprunt',
            "borrows": new_borrows,
        }
        return render(request, 'borrow/borrows.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def edit_borrow(request, id):
    if request.user.has_perm('borrow.change_borrow'):
        if request.user.is_superuser:
            livre = Book.objects.filter(status=1)
            read = Reader.objects.filter(status=1).filter(type_Reader=2)
        else:
            livre = Book.objects.filter(status=1).filter(category__rayon__readpoint_id=request.user.readpoint.pk)
            read = Reader.objects.filter(status=1).filter(readpoint=request.user.readpoint).filter(type_Reader=2)

        borrow = Borrow.objects.get(pk=id)
        read_selected = Reader.objects.filter(pk=borrow.reader.pk).filter(type_Reader=2)
        book_selected = Book.objects.get(pk=borrow.book.pk)
        read_selected = read_selected[0].pk
        book_selected = book_selected.pk
        if request.method == "POST":
            read_selected = int(request.POST['reader']) if request.POST['reader'] != '' else ''
            book_selected = int(request.POST['reader']) if request.POST['reader'] != '' else ''
            borrowForm = BorrowForm(request.POST, instance=borrow)
            if borrowForm.is_valid():
                if request.POST['reader'] == '':
                    messages.error(request,
                                   "Veuillez Selection un lecteur",
                                   fail_silently=True
                                   )
                    return render(request, 'borrow/editborrow.html',
                                  {'form': borrowForm,
                                   'reader': read,
                                   'book': livre,
                                   'book_selected': book_selected,
                                   'read_selected': read_selected,
                                   'tooltip': 'Modification Emprunt'})
                if request.POST['book'] == '':
                    messages.error(request,
                                   "Veuillez selectionner un livre.",
                                   fail_silently=True
                                   )
                    return render(request, 'borrow/editborrow.html',
                                  {'form': borrowForm,
                                   'reader': read,
                                   'book': livre,
                                   'book_selected': book_selected,
                                   'read_selected': read_selected,
                                   'tooltip': 'Modification Emprunt'})

                if borrowForm.cleaned_data['date_borrow'] > date.today():
                    messages.error(request,
                                   "Erreur edit d'emprunt la date debut d'emprunt doit être inferieur ou egale a la date d'aujourd'hui Veuillez ressayer.",
                                   fail_silently=True
                                   )
                    return render(request, 'borrow/editborrow.html',
                                  {'form': borrowForm,
                                   'reader': read,
                                   'book': livre,
                                   'book_selected': book_selected,
                                   'read_selected': read_selected,
                                   'tooltip': 'Modification Emprunt'})
                elif borrowForm.cleaned_data['expired_date_borrow'] < date.today():
                    messages.error(request,
                                   "Erreur edit d'emprunt la date fin d'emprunt doit être superieur  a la date d'aujourd'hui Veuillez ressayer.",
                                   fail_silently=True
                                   )
                    return render(request, 'borrow/editborrow.html',
                                  {'form': borrowForm, 'tooltip': 'Modification Emprunt',
                                   'reader': read,
                                   'book': livre,
                                   'book_selected': book_selected,
                                   'read_selected': read_selected})
                else:
                    borr = borrowForm.save(commit=False)
                    borr.modified_by = request.user.id
                    borr.reader_id = int(request.POST['reader'])
                    borr.book_id = int(request.POST['book'])
                    borr.save()
                    messages.success(request,
                                     "Modification effectuée avec succés",
                                     fail_silently=True
                                     )
                    return redirect('borrows')
            else:
                messages.error(request,
                               "Erreur d'emprunt verifier bien le formulaire.",
                               fail_silently=True
                               )
                return render(request, 'borrow/editborrow.html',
                              {
                                  'form': borrowForm, 'tooltip': 'Modification Emprunt',
                                  'reader': read,
                                  'book': livre,
                                  'book_selected': book_selected,
                                  'read_selected': read_selected})
        else:
            borrowForm = BorrowForm(instance=borrow)
            context = {
                'tooltip': "Edition des emprunt",
                'form': borrowForm,
                'reader': read,
                'book': livre,
                'book_selected': book_selected,
                'read_selected': read_selected
            }
            return render(request, 'borrow/editborrow.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def delete_borrow(request, id):
    if request.user.has_perm('borrow.delete_borrow'):
        borrow = Borrow.objects.get(pk=id)
        borrow.status = 0
        borrow.save()
        messages.info(request,
                      "suppression effectuée avec succés",
                      fail_silently=True
                      )
        return redirect('borrows')
    else:
        return redirect('home_site')


@login_required(login_url='login')
def returns(request, id):
    if request.user.is_superuser:
        borrows = Borrow.objects.filter(status=1).filter(pk=id)
    else:
        borrows = Borrow.objects.filter(status=1).filter(
            book__category__rayon__readpoint_id=request.user.readpoint.pk).filter(pk=id)
    borrows = borrows[0]
    context = {
        'tooltip': "Enregistrement d'un retour",
        'borrow': borrows
    }
    return render(request, 'borrow/returns.html', context)


@login_required(login_url='login')
def changeBorrowStatus(request, id):
    if request.user.has_perm('borrow.change_borrow'):
        borrow = Borrow.objects.get(pk=id)
        borrow.status = 2
        borrow.return_date_borrow = date.today()
        borrow.modified_by = request.user.id
        if not borrow.save():
            book = Book.objects.get(pk=borrow.book.pk)
            book.number_copy_book += 1;
            book.save()
            form = Movement_form({
                'book': book,
                'quantite': 1,
                'motif': "Retour d'Emprunt",
                'type': 4
            })
            if form.is_valid():
                if form.save():
                    messages.success(request,
                                     "restituer avec succés",
                                     fail_silently=True
                                     )
                    return redirect('borrows')
            else:
                messages.error(request,
                               "Error de restitution d'emprunt",
                               fail_silently=True
                               )
                return redirect('borrows')
    else:
        return redirect('home_site')


@login_required(login_url='login')
def liste_borrow_return(request):
    if request.user.has_perm('borrow.view_borrow'):
        if request.user.is_superuser:
            borrows = Borrow.objects.filter(status=2)
        else:
            borrows = Borrow.objects.filter(status=2).filter(book__category__rayon__readpoint=request.user.id)
        context = {
            'tooltip': "liste des emprunts",
            'borrow': borrow,
            'borrows': borrows
        }
        return render(request, 'borrow/liste_borrow_return.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def retour(request):
    if request.user.has_perm('borrow.view_borrow'):
        if request.method == 'POST':
            retourForm = RetourForm(request.POST)
            if retourForm.is_valid():
                reader = retourForm.cleaned_data['idReader']
                borrows = Borrow.objects.filter(reader=reader).filter(status=1)
                new_borrows = []
                for borrow in borrows:
                    b = {
                        'pk': borrow.pk,
                        'date_borrow': borrow.date_borrow,
                        'expired_date_borrow': borrow.expired_date_borrow,
                        'return_date_borrow': borrow.return_date_borrow,
                        'reader': borrow.reader,
                        'book': borrow.book,
                        'stat': borrow.expired_date_borrow > date.today(),
                        'days': (borrow.expired_date_borrow - date.today()).days
                    }
                    new_borrows.append(b)
                context = {
                    'tooltip': 'Retour des emprunts',
                    "borrows": new_borrows,
                    "borrow": retourForm
                }
                return render(request, 'borrow/retour.html', context)
        else:
            retourForm = RetourForm()
            context = {
                'tooltip': 'Retour des emprunts',
                'borrow': retourForm
            }
            return render(request, 'borrow/retour.html', context)
    else:
        return redirect('home_site')



# importing the necessary libraries
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        # changer la requette
        if request.user.has_perm('borrow.view_borrow'):
            if request.user.is_superuser:
                borrows = Borrow.objects.filter(status=1)
            else:
                borrows = Borrow.objects.filter(status=1).filter(
                    book__category__rayon__readpoint=request.user.readpoint.pk)
        # changer le chemin du temble
        pdf = html_to_pdf('borrow/printBorrow.html', {
            # on change la cle de la variable de parcours dans le templete pour la boubcle for
            "borrow": borrows,
            # le tooltip
            "title":'Liste Des Emprunt'
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
        # rendering the template
        return HttpResponse(response, content_type='application/pdf')


class GenerateRetourPdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        # changer la requette
        if request.user.has_perm('borrow.view_borrow'):
            if request.user.is_superuser:
                borrows = Borrow.objects.filter(status=2)
            else:
                borrows = Borrow.objects.filter(status=2).filter(book__category__rayon__readpoint=request.user.id)

        # changer le chemin du temble
        pdf = html_to_pdf('borrow/printBorrowRetour.html', {
            # on change la cle de la variable de parcours dans le templete pour la boubcle for
            "borrows": borrows,
            # le tooltip
            "title":'Liste Des Emprunt retournés'
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
        # rendering the template
        return HttpResponse(response, content_type='application/pdf')
