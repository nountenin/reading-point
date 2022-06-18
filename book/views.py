# Create your views here.
import json
#from crispy_forms.layout import HTML
from crispy_forms.layout import HTML
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# from django_weasyprint import WeasyTemplateResponseMixin
# from django_weasyprint.views import WeasyTemplateResponse

import pdfkit
from wkhtmltopdf import wkhtmltopdf
from wkhtmltopdf.views import PDFTemplateResponse

from book.forms import BookForm, Category_form, Author_form, Movement_form, Movement_form_filtre
from book.forms import ReadPoint_form, Rayon_form
from book.models import Book, Category, Author, Movement, Transfert, Item_transfert
from book.models import ReadPoint, Rayon
from book.serializers import ReadPointSerializer, ApiReadPoint, ApiCate, Category_api
from borrow.models import Parametre
from library_gn import settings


@login_required(login_url='login')
def dashboard(request):
    context = {
        'tooltip': 'Tableau de bord',
        'session': request
    }
    return render(request, 'book/dashboard.html', context)


id_user = 0


@login_required(login_url='login')
def ranks(request):
    add = request.user.has_perm('book.add_rayon')
    delete = request.user.has_perm('book.delete_rayon')
    change = request.user.has_perm('book.change_rayon')
    if request.user.is_superuser:
        list_ranks = Rayon.objects.exclude(status=0)
        form_readpoint = ReadPoint.objects.filter(status=1)
    else:
        list_ranks = Rayon.objects.exclude(status=0).filter(readpoint_id=request.user.readpoint.pk)
        form_readpoint = ReadPoint.objects.filter(status=1).filter(pk=request.user.readpoint.pk)
    if request.method == "POST":
        form = Rayon_form(request.POST)
        if request.user.has_perm('book.add_rayon'):
            if form.is_valid():
                rayon = Rayon.objects.filter(status=1).filter(name_rayon=request.POST['name_rayon']).filter(
                    readpoint=request.POST['readpoint'])
                if rayon:
                    messages.error(request, "Ce rayon existe déjà dans ce point de lecture")
                    return render(request, 'book/ranks.html', context={'ranks': form,
                                                                       'add': add,
                                                                       'delete': delete,
                                                                       'change': change,
                                                                       'form_readpoint': form_readpoint,
                                                                       "list_ranks": list_ranks,
                                                                       'tooltip': 'Liste des Rayons'})
                rayon = form.save(commit=False)
                rayon.created_by = request.user.id
                rayon.save()
                messages.success(request, "Nouveau Rayon Créé")
                return redirect("ranks")
            else:
                messages.error(request, "Erreur d'ajout vérifier bien le formulaire")
                return render(request, 'book/ranks.html', context={'ranks': form,
                                                                   'add': add,
                                                                   'delete': delete,
                                                                   'change': change,
                                                                   'form_readpoint': form_readpoint,
                                                                   "list_ranks": list_ranks,
                                                                   'tooltip': 'Liste des Rayons'})
        else:
                        return redirect('home_site')
    else:
        form = Rayon_form()

        if request.user.has_perm('book.view_rayon'):
            return render(request, 'book/ranks.html', context={'ranks': form,
                                                               "list_ranks": list_ranks,
                                                               'add': add,
                                                               'delete': delete,
                                                               'change': change,
                                                               'tooltip': 'Liste des Rayons',
                                                               'form_readpoint': form_readpoint,
                                                               "rp_only": ReadPoint.objects.filter(status=1)})
        else:
                        return redirect('home_site')


@login_required(login_url='login')
def delete_rank(request, id):
    if request.user.has_perm('book.delete_rayon'):
        res = Rayon.objects.get(id=id)
        res.status = 0
        res.save()
        messages.success(request, "Suppression effectuée")
        return redirect('ranks')
    else:
        return redirect('home_site')


@login_required(login_url='login')
def read_points(request):
    add = request.user.has_perm('book.add_readpoint');
    change = request.user.has_perm('book.change_readpoint');
    delete = request.user.has_perm('book.delete_readpoint');
    if request.user.is_superuser:
        readPoints = ReadPoint.objects.exclude(status=0)
    else:
        readPoints = ReadPoint.objects.exclude(status=0).filter(pk=request.user.readpoint.pk)
    if request.method == "POST":
        if request.user.has_perm('book.add_readpoint'):
            form = ReadPoint_form(request.POST)
            if form.is_valid():
                contact = ReadPoint.objects.filter(contact1_readpoint=form.cleaned_data['contact1_readpoint']).filter(
                    status=1)
                contact2 = ReadPoint.objects.filter(contact2_readpoint=form.cleaned_data['contact1_readpoint']).filter(
                    status=1)
                readPoint = ReadPoint.objects.filter(name_readpoint=form.cleaned_data['name_readpoint']).filter(
                    status=1)
                et = True
                email = ReadPoint.objects.filter(email_readpoint=form.cleaned_data['email_readpoint']).filter(status=1)
                valide = True
                if readPoint:
                    messages.error(request, "Ce point de lecture existe déjà ")
                    return render(request, 'book/readpoints.html', context={'form': form, "readPoints": readPoints})
                if email:
                    valide = False
                    messages.error(request, "Cet email existe déjà")
                if contact:
                    valide = False
                    messages.error(request, "Ce Contact1 existe déjà")
                if contact2:
                    valide = False
                    messages.error(request, "Ce Contact2 existe déjà ")
                if not valide:
                    return render(request, 'book/readpoints.html', context={'form': form, "readPoints": readPoints})
                else:
                    readPoint = form.save(commit=False)
                    readPoint.created_by = request.user.id
                    if not readPoint.save():

                        messages.info(request, "Nouveau Point de lecture créé")
                        parametre = Parametre(readPoint=readPoint)
                        parametre.save()
                        return render(request, 'book/readpoints.html',
                                      context={'form': ReadPoint_form(),
                                               "access": add,
                                               "change": change,
                                               "delete": delete,
                                               "readPoints": readPoints,
                                               'tooltip': 'Liste des points de lectures'
                                               })
                    else:
                        messages.error(request, "Erreur d'insertion verifier bien le formulaire")
                        return render(request, 'book/readpoints.html', context={'form': form,
                                                                                "access": add,
                                                                                "change": change,
                                                                                "delete": delete,
                                                                                "readPoints": readPoints,
                                                                                'tooltip': 'Liste des points de lectures'})
            else:
                messages.error(request, "Erreur d'insertion verifier bien le formulaire")
                return render(request, 'book/readpoints.html', context={'form': form, "access": add,
                                                                        "access": add,
                                                                        "change": change,
                                                                        "delete": delete,
                                                                        "readPoints": readPoints,
                                                                        'tooltip': 'Liste des points de lectures'})
        else:
            return redirect('home_site')

    else:
        if request.user.has_perm('book.view_readpoint'):
            form = ReadPoint_form()
            return render(request, 'book/readpoints.html', context={"form": form,
                                                                    "access": add,
                                                                    "change": change,
                                                                    "delete": delete,
                                                                    "readPoints": readPoints,
                                                                    'tooltip': 'Liste des points de lectures'})
        else:
            return redirect('home_site')


@login_required(login_url='login')
def delete_read_point(request, id):
    if request.user.has_perm('book.delete_readpoint'):
        id = ReadPoint.objects.get(id=id)
        id.status = 0
        id.save()
        messages.info(request, "Suppression effectuée")
        return redirect("readpoints")
    else:
        messages.error(request, "Vous n'avez pas le droit de supprimer un point de lecture")
        return redirect('home_site')


@login_required(login_url='login')
def edit_read_point(request, id):
    if request.user.has_perm('book.change_readpoint'):
        rp = ReadPoint.objects.get(id=id)
        if request.method == "POST":
            form = ReadPoint_form(request.POST, instance=rp)
            if form.is_valid():
                contact = ReadPoint.objects.filter(contact1_readpoint=form.cleaned_data['contact1_readpoint']).exclude(
                    pk=id).filter(status=1)
                contact2 = ReadPoint.objects.filter(contact2_readpoint=form.cleaned_data['contact1_readpoint']).exclude(
                    pk=id).filter(status=1)
                email = ReadPoint.objects.filter(email_readpoint=form.cleaned_data['email_readpoint']).exclude(
                    pk=id).filter(status=1)
                readPoint = ReadPoint.objects.filter(name_readpoint=form.cleaned_data['name_readpoint']).exclude(
                    pk=id).filter(status=1)
                valide = True
                if readPoint:
                    messages.error(request, "Erreur de Modification car ce point de lecture existe ")
                    return render(request, 'book/edit_read_point.html', {'rp': rp})
                if email:
                    valide = False
                    messages.error(request, "Cet email existe déjà")
                if contact:
                    valide = False
                    messages.error(request, "Erreur de Modification car contact1 existe")
                if contact2:
                    valide = False
                    messages.error(request, "Erreur de Modification car contact2 existe ")
                if not valide:
                    return render(request, 'book/edit_read_point.html', {'rp': rp})
                else:
                    readpoint = form.save(commit=False)
                    readpoint.modified_by = request.user.id
                    if not readpoint.save():
                        messages.info(request, "Modification effectuée avec succés")
                        return redirect('readpoints')
        else:
            return render(request, 'book/edit_read_point.html', {'rp': rp})
    else:
        messages.error(request, "Vous n'avez pas le droit de modifier un point de lecture")
        return redirect('home_site')


@login_required(login_url='login')
def edit_rank(request, id):
    if request.user.has_perm('book.change_rayon'):
        rk = Rayon.objects.get(id=id)
        rp = ReadPoint.objects.get(pk=rk.readpoint.pk)
        read_p = Rayon_form(instance=rk)
        if request.user.is_superuser:
            readpoint = ReadPoint.objects.filter(status=1)
        else:
            readpoint = ReadPoint.objects.filter(pk=request.user.readpoint.pk).filter(status=1)
        if request.method == "POST":
            rank = Rayon_form(request.POST, instance=rk)
            if rank.is_valid:
                rayon = rank.save(commit=False)
                rayon.modified_by = request.user.id
                rayon.save()
                messages.success(request, "Modification effectuée")
                return redirect("ranks")
            messages.success(request, "Erreur de Modification vérifier bien le formulaire")
            return render(request, 'book/edit_rank.html', {'rk': rk,
                                                           'rp': rp,
                                                           'readpoint': readpoint,
                                                           "read_p_rk": read_p})
        else:
            return render(request, 'book/edit_rank.html', {'rk': rk,
                                                           'rp': rp,
                                                           'readpoint': readpoint,
                                                           "read_p_rk": read_p})

    else:
        return redirect('home_site')


@login_required(login_url='login')
def edit(request, id):
    context = {
        'tooltip': 'Livres',

    }
    return render(request, 'book/books.html', context)


@login_required(login_url='login')
def filtrer_rank(request, id):
    if request.method == "GET":
        rank_f = Rayon.objects.filter(readpoint=id)
        return render(request, "book/ranks.html", context={"list_ranks": rank_f})
    else:
        return render(request, "book/ranks.html", context={"list_ranks": Rayon.objects.all()})


@login_required(login_url='login')
def detail_book(request, id):
    if request.user.has_perm('book.view_book'):
        book = Book.objects.get(pk=id)
        context = {
            'tooltip': 'Détail du livre',
            'book': book
        }
        return render(request, 'book/detail_book.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def books(request):
    add = request.user.has_perm('book.add_book')
    delete = request.user.has_perm('book.delete_book')
    change = request.user.has_perm('book.change_book')
    voir = request.user.has_perm('book.view_book')
    if request.user.is_superuser:
        books = Book.objects.filter(status=1)
    else:
        books = Book.objects.exclude(status=0).all().filter(category__rayon__readpoint_id=request.user.readpoint.pk)

    context = {
        'tooltip': 'Livres',
        'add': add,
        'change': change,
        'delete': delete,
        'voir': voir,
        'books': books
    }
    return render(request, 'book/books.html', context)
@login_required(login_url='login')
def allbooks(request):
    books = Book.objects.filter(status=1)

    context = {
        'tooltip': 'Liste de tous les livres',
        'books': books
    }
    return render(request, 'book/allbooks.html', context)


@login_required(login_url='login')
def add_book(request):
    if request.user.has_perm('book.add_book'):
        if request.user.is_superuser:
            categorie = Category.objects.filter(status=1)
        else:
            categorie = Category.objects.filter(status=1).filter(rayon__readpoint_id=request.user.readpoint.pk)

        if request.method == "POST":
            form = BookForm(request.POST, request.FILES)
            category_selected = int(request.POST['category']) if request.POST['category'] != '' else ''
            if form.is_valid():

                book = Book.objects.filter(isbn_book=request.POST['isbn_book']).filter(
                    category=request.POST['category']).filter(status=1)
                if book:
                    messages.info(request, "Ce livre existe voulez vous l'approvisionner?")

                    context = {
                        'tooltip': 'Ajout Livres',
                        'id': book[0].pk,
                        'quantite': request.POST['number_copy_book'],
                        'form': form,
                        'category': categorie,
                        'category_selected': category_selected
                    }
                    return render(request, 'book/add_book.html', context)
                else:

                    livre = form.save(commit=False)
                    livre.created_by = request.user.id
                    if not livre.save():
                        livre = Book.objects.latest('id')
                        forms = Movement_form({
                            'book': livre,
                            'quantite': request.POST['number_copy_book'],
                            'motif': "Stock initiale",
                            'type': 1
                        })

                    if forms.is_valid():

                        movement = forms.save(commit=False)
                        movement.created_by = request.user.id
                        if not movement.save():
                            messages.success(request,
                                             "Livre ajouté avec succés",
                                             fail_silently=True
                                             )
                            return render(request, 'book/add_book.html',
                                          {'form': BookForm(), 'tooltip': 'Ajout Livre', 'category': categorie, })
                        else:
                            messages.error(request,
                                           "Livre ajouté mais echec d'enregistrement de  mouvement",
                                           fail_silently=True
                                           )
                            return render(request, 'book/add_book.html',
                                          {'form': form, 'tooltip': 'Ajout Livre', 'category': categorie, })
                    else:
                        messages.error(request,
                                       "Livre ajouté mais echec d'enregistrement de  mouvement car ces donnée sont invalid",
                                       fail_silently=True
                                       )
                        return render(request, 'book/add_book.html',
                                      {'form': BookForm(), 'tooltip': 'Ajout Livres', 'category': categorie, })
            messages.error(request, "Erreur d'ajout veillez verifier bien le formulaire")
            category_selected = int(request.POST['category'])
            return render(request, 'book/add_book.html',
                          {'form': form, 'category': categorie, 'category_selected': category_selected, })

        else:
            form = BookForm()
            context = {
                'tooltip': 'Ajout Livres',
                'form': form,
                'category': categorie
            }
            return render(request, 'book/add_book.html', context)
    else:
                return redirect('home_site')


@login_required(login_url='login')
def delete_book(request, id):
    if request.user.has_perm('book.delete_book'):
        book = Book.objects.get(pk=id)
        book.status = 0
        book.save()
        messages.success(request, "suppression effectuée avec succés")
        return redirect('books')
    else:
        return redirect('home_site')


@login_required(login_url='login')
def edit_book(request, id):
    if request.user.has_perm('book.change_book'):
        instance = get_object_or_404(Book, id=id)
        category_selected = Category.objects.get(pk=instance.category_id)
        if request.user.is_superuser:
            categorie = Category.objects.filter(status=1)
        else:
            categorie = Category.objects.filter(status=1).filter(rayon__readpoint_id=request.user.readpoint.pk)
        category_selected = category_selected.pk
        if request.method == 'POST':
            book = BookForm(request.POST or None, request.FILES, instance=instance)
            if request.POST['category'] == '' :
                messages.error(request, "Veillez selectionner une categorie?")
                context = {
                        'tooltip': 'Ajout Livres',
                        'form': book,
                        'category_selected': category_selected,
                        'category': categorie
                    }
                return render(request, 'book/edit_book.html', context)
            category_selected = int (request.POST['category'])
            books = Book.objects.filter(isbn_book=request.POST['isbn_book']).filter(category_id=int(request.POST['category'])).exclude(isbn_book=instance.isbn_book)
            if books:
                messages.error(request, "Ce livre existe voulez vous l'approvisionner?")
                context = {
                    'tooltip': 'Ajout Livres',
                    'form': book,
                    'category_selected': category_selected,
                    'category': categorie
                }
                return render(request, 'book/edit_book.html', context)

            else:
                if book.is_valid():
                    boo =  book.save(commit=False)
                    boo.modified_by = request.user.id
                    boo.save()
                    messages.success(request, "Modification effectuée avec succés")
                    return redirect('books')
                else:
                    messages.error(request, 'Erreur de modification verifier bien votre formulaire')
                    context = {
                        'tooltip': 'Modification Livres',
                        'form': book,
                        'category_selected': category_selected,
                        'category': categorie
                    }
                    return render(request, 'book/edit_book.html', context)
        else:
            book = Book.objects.get(pk=id)
            formbook = BookForm(instance=book)
            context = {
                'tooltip': 'Modification',
                'form': formbook,
                'category_selected': category_selected,
                'category': categorie
            }
            return render(request, 'book/edit_book.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def category(request):
    add = request.user.has_perm('book.add_category')
    delete = request.user.has_perm('book.delete_category')
    change = request.user.has_perm('book.change_category')
    voir = request.user.has_perm('book.view_category')

    if request.user.is_superuser:
        rayon = Rayon.objects.filter(status=1)
        categor = Category.objects.filter(status=1)
    else:
        rayon = Rayon.objects.filter(readpoint=request.user.readpoint.pk)
        categor = Category.objects.filter(status=1).filter(rayon__readpoint=request.user.readpoint.pk)
    if request.method == 'POST':
        problem = False
        if add:
            if request.POST['rayon'] == '':
                messages.error(request, "Veiullez selectionnez un rayon")
                problem = True
            category = Category.objects.filter(status=1).filter(name_category=request.POST['name_category']).filter(
                rayon__readpoint_id=request.user.readpoint.pk)
            if category:
                messages.error(request, "Cette category existe déjà")
                problem = True
            if problem:
                return redirect('category')
            form = Category_form(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.rayon_id = int(request.POST['rayon'])
                category.created_by = request.user.id
                if not category.save():
                    messages.success(request, "Catégorie ajoutée avec succés")
                    return redirect('category')
                else:
                    messages.error(request, "Erreur d'ajout de la Catégorie")
                    return redirect('category')
            else:
                messages.error(request, "Erreur d'ajout verifier bien votre formulaire")
                return redirect('category')
        else:
            return redirect('home_site')
    else:
        if voir or add:
            form = Category_form()
            context = {
                'tooltip': 'Catégorie', 'add': add,
                'change': change,
                'delete': delete,
                'voir': voir,
                'categories': categor,
                'form_rayon': rayon,
                'form': form
            }
            return render(request, 'book/category.html', context)
        else:
            return redirect('home_site')


@login_required(login_url='login')
def delete_category(request, id):
    if request.user.has_perm('book.delete_category'):
        categorys = Category.objects.get(pk=id)
        categorys.status = 0
        categorys.save()
        messages.info(request, "Catégorie supprimée avec succés")
        return redirect('category')
    else:
        return redirect('home_site')


@login_required(login_url='login')
def edit_category(request, id):
    add = request.user.has_perm('book.add_category')
    delete = request.user.has_perm('book.delete_category')
    change = request.user.has_perm('book.change_category')
    voir = request.user.has_perm('book.view_category')
    if request.user.has_perm('book.change_category'):
        categories = Category.objects.filter(status=1)
        instance = get_object_or_404(Category, id=id)
        if request.user.is_superuser:
            rayon = Rayon.objects.filter(status=1)
        else:
            rayon = Rayon.objects.filter(status=1).filter(readpoint=request.user.readpoint.pk)
        rayon_selected = Rayon.objects.get(pk=instance.rayon.pk)
        if request.method == 'POST':
            categorys = Category_form(request.POST or None, instance=instance)
            if categorys.is_valid():
                categorie = categorys.save(commit=False)
                categorie.created_by = request.user.id
                if not categorie.save():
                    messages.success(request, "Modification effectuée avec succés")
                    return redirect('category')
            else:
                messages.error(request, "Erreur de Modification")
                context = {
                    'tooltip': 'Catégorie',
                    'form_rayon': rayon,
                    'form': categorys,
                    'categories': categories,
                    'rayon_selected': rayon_selected,
                    'add': add,
                    'change': change,
                    'delete': delete,
                    'voir': voir,
                }
                return render(request, 'book/category.html', context)
        elif id != 0:
            categorys = Category.objects.get(pk=id)
            form_category = Category_form(instance=categorys)
            context = {
                'tooltip': 'Categorie',
                'form': form_category,
                'rayon_selected': rayon_selected,
                'form_rayon': rayon,
                'categories': categories,
                'add': add,
                'change': change,
                'delete': delete,
                'voir': voir,
            }
            return render(request, 'book/category.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def author(request):
    user = request.user
    add = user.has_perm('book.add_author')
    delete = user.has_perm('book.delete_author')
    change = user.has_perm('book.change_author')
    voir = user.has_perm('book.view_author')
    if user.is_superuser:
        authors = Author.objects.all().exclude(status=0)
    else:
        authors = Author.objects.filter(status=1).filter(book__category__rayon__readpoint=request.user.id)
    if request.method == 'POST':
        if user.has_perm('book.add_author'):
            form = Author_form(request.POST)
            if form.is_valid():
                auteur = form.save(commit=False)
                auteur.created_by = user.id
                if not auteur.save():
                    messages.success(request, "Auteur ajouté avec succés")
                    return redirect('author')
                else:
                    messages.error(request, "Erreur d'ajout")
                    context = {
                        'tooltip': 'Auteur',
                        'form': Author_form(),
                    }
                    return render(request, 'book/author.html', context)
            else:
                messages.error(request, "Erreur d'ajout verifier bien votre formulaire")
                context = {
                    'tooltip': 'Auteur',
                    'form': Author_form(),
                }
                return render(request, 'book/auteur.html', context)
        else:
            return redirect('home_site')
    else:
        form = Author_form()
        context = {
            'tooltip': 'Auteurs',
            'change': change,
            'add': add,
            'delete': delete,
            'voir': voir,
            'authors': authors,
            'form': form
        }
        return render(request, 'book/author.html', context)


@login_required(login_url='login')
def delete_author(request, id):
    if request.user.has_perm('book.delete_author'):
        authors = Author.objects.get(pk=id)
        authors.status = 0
        authors.save()
        messages.info(request, "Suppression effectuée avec succés")
        return redirect('author')
    else:
        return redirect('home_site')


@login_required(login_url='login')
def edit_author(request, id):
    if request.user.has_perm('book.change_author'):
        instance = get_object_or_404(Author, id=id)
        authors = Author_form(request.POST or None, instance=instance)
        if request.method == 'POST':

            if authors.is_valid():
                auteur = authors.save(commit=False)
                auteur.modified_by = request.user.id
                if not auteur.save():
                    messages.success(request, "Modification effectuée avec succés")
                    return redirect('author')
                else:
                    messages.error(request, "Erreur de modification verifier bien votre formulaire")
                    context = {
                        'tooltip': 'Edit Auteur',
                        'form': authors,
                    }
                    return render(request, 'book/auteur.html', context)
            else:
                messages.error(request, "Erreur de modification verifier bien votre formulaire")
                context = {
                    'tooltip': 'Edit Auteur',
                    'form': authors,
                }
                return render(request, 'book/auteur.html', context)

        else:
            authors = Author.objects.get(pk=id)
            form = Author_form(instance=authors)
            authors = Author.objects.all()
            context = {
                'tooltip': 'Auteurs',
                'form': form,
                'authors': authors
            }
            return render(request, 'book/author.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def movement(request):
    add = request.user.has_perm('book.add_movement')
    if add:
        voir = request.user.has_perm('book.view_movement')
        if request.user.is_superuser:
            livre = Book.objects.filter(status=1)
        else:
            livre = Book.objects.filter(status=1).filter(category__rayon__readpoint_id=request.user.readpoint_id)
        if request.method == 'POST':
            form = Movement_form(request.POST)
            if form.is_valid():
                movement = form.save(commit=False)
                movement.created_by = request.user.id
                if not movement.save():
                    messages.success(request, "Mouvement ajouté avec succés")
                    return redirect('movement')
            messages.error(request, "Erreur d'ajout du mouvement")
            return redirect('movement')
        else:
            form = Movement_form()
            context = {
                'add': add,
                'voir': voir,
                'tooltip': 'Mouvements',
                'form': form,
                'livre': livre
            }
            return render(request, 'book/movement.html', context)
    else:
                return redirect('home_site')


@login_required(login_url='login')
def edit_movement(request, id):
    if request.user.has_perm('book.change_movement'):
        voir = request.user.has_perm('book.view_movement')
        add = request.user.has_perm('book.add_movement')
        instance = get_object_or_404(Movement, id=id)
        book_selected = Book.objects.get(pk=instance.book_id)
        if request.user.is_superuser:
            livre = Book.objects.filter(status=1)
        else:
            livre = Book.objects.filter(status=1).filter(category_rayon_readpoint_id=request.user.readpoint_id)
        if request.method == 'POST':
            movements = Movement_form(request.POST or None, instance=instance)
            if movements.is_valid():
                mov = movements.save(commit=False)
                mov.modified_by = request.user.id
                mov.save()
                messages.success(request, 'Movement Modifié avec succès')
                return redirect('movement')
        elif id != 0:
            movements = Movement.objects.get(pk=id)
            form = Movement_form(instance=movements)
            movements = Movement.objects.all()
            context = {
                'tooltip': 'Modification du mouvement',
                'form': form,
                'movements': movements,
                'book_selected': book_selected,
                'add': add,
                'livre': livre,
                'voir': voir
            }
            return render(request, 'book/movement.html', context)
    else:
        return redirect('home_site')


@login_required(login_url='login')
def delete_movement(request, id):
    if request.user.has_perm('book.delete_movement'):
        movements = Movement.objects.get(pk=id)
        movements.status = 0
        messages.info(request, "Suppression effectuée avec succès")
        movements.save()
        return redirect('list_movement')
    else:
        return redirect('home_site')


@login_required(login_url='login')
def detail_movement(request, id):
    if request.user.has_perm('book.view_movement'):
        move = Movement.objects.get(pk=id)
        context = {
            'tooltip': 'Détail du movement',
            'move': move
        }
        return render(request, 'book/detail_movement.html', context)

    else:
        return redirect('home_site')


@login_required(login_url='login')
def list_movement(request):
    voir = request.user.has_perm('book.view_movement')
    if voir:
        change = request.user.has_perm('book.change_movement')
        delete = request.user.has_perm('book.delete_movement')
        titlemov = Movement.objects.filter(status=1).values('book').annotate(code=Count('id')).filter(
            book__category__rayon__readpoint_id=request.user.readpoint.pk)
        date_move = Movement.objects.filter(status=1).values('date_movement').annotate(code=Count('id'))
        book = []
        for livre in titlemov:
            l = Book.objects.get(pk=livre['book'])
            book.append(l)
        if request.method == "POST":
            dates = request.POST['date_movement']
            type = request.POST['type']
            title = request.POST['title_book']
            if dates == '':

                if type == '':
                    if title == '':
                        movements = Movement.objects.all().filter(status=1)
                        movements_result = movements
                        # messages.error(request, "vide")
                        movements = Movement.objects.filter(status=1)
                        context = {
                            'tooltip': 'Liste des mouvements',
                            'form': Movement_form_filtre(),
                            'list_move': movements_result,
                            'dates': date_move,
                            'title': book,
                            'list_movement': movements
                        }
                        return render(request, 'book/list_movement.html', context)
                    movements = Movement.objects.all().filter(status=1)
                    movements_result = movements.filter(book_id=request.POST['title_book'])
                    if movements_result:
                        movements = Movement.objects.filter(status=1)
                        context = {
                            'tooltip': 'Liste des mouvements',
                            'list_move': movements_result,
                            'form': Movement_form_filtre(),
                            'dates': date_move,
                            'title': book,
                            'list_movement': movements
                        }
                        return render(request, 'book/list_movement.html', context)
                    else:
                        messages.success(request, "vide")
                        return redirect('list_movement')
                elif title == '':
                    movements_result = Movement.objects.all().filter(status=1).filter(type=request.POST['type'])
                    if movements_result:
                        movements = Movement.objects.filter(status=1)
                        context = {
                            'tooltip': 'Liste des mouvements',
                            'list_move': movements_result,
                            'form': Movement_form_filtre(),
                            'dates': date_move,
                            'title': book,
                            'list_movement': movements
                        }
                        return render(request, 'book/list_movement.html', context)
                    else:
                        messages.success(request, "vide")
                        return redirect('list_movement')
                movements = Movement.objects.all().filter(status=1).filter(type=request.POST['type'])
                movements_result = movements.filter(book_id=request.POST['title_book'])
                if movements_result:
                    movements = Movement.objects.filter(status=1)
                    context = {
                        'tooltip': 'Liste des mouvements',
                        'list_move': movements_result,
                        'form': Movement_form_filtre(),
                        'dates': date_move,
                        'title': book,
                        'list_movement': movements
                    }
                    return render(request, 'book/list_movement.html', context)
                else:
                    messages.success(request, "vide")
                    return redirect('list_movement')
            elif type == '':
                if dates == '':
                    movements = Movement.objects.all().filter(status=1)
                    movements_result = movements.filter(book_id=request.POST['title_book'])
                    if movements_result:
                        movements = Movement.objects.filter(status=1)
                        context = {
                            'tooltip': 'Liste des mouvements',
                            'list_move': movements_result,
                            'form': Movement_form_filtre(),
                            'dates': date_move,
                            'title': book,
                            'list_movement': movements
                        }
                        return render(request, 'book/list_movement.html', context)
                    else:
                        messages.success(request, "vide")
                        return redirect('list_movement')
                elif title == '':
                    movements = Movement.objects.all().filter(status=1).filter(
                        date_movement=request.POST['date_movement'])
                    movements_result = movements
                    if movements_result:
                        movements = Movement.objects.filter(status=1)
                        context = {
                            'tooltip': 'Liste des mouvements',
                            'list_move': movements_result,
                            'form': Movement_form_filtre(),
                            'dates': date_move,
                            'title': book,
                            'list_movement': movements
                        }
                        return render(request, 'book/list_movement.html', context)
                    else:
                        messages.success(request, "vide")
                        return redirect('list_movement')
                movements = Movement.objects.filter(book_id = request.POST['title_book']).filter(date_movement=request.POST['date_movement'])
                movements_result = movements
                if movements_result:
                    movements = Movement.objects.filter(status=1)
                    context = {
                        'tooltip': 'Liste des mouvements',
                        'list_move': movements_result,
                        'form': Movement_form_filtre(),
                        'dates': date_move,
                        'title': book,
                        'list_movement': movements
                    }
                    return render(request, 'book/list_movement.html', context)
                else:
                    messages.success(request, "vide")
                    return redirect('list_movement')
            elif title == '':
                if dates == '':
                    movements = Movement.objects.all().filter(status=1).filter(type=request.POST['type'])
                    movements_result = movements
                    if movements_result:
                        movements = Movement.objects.filter(status=1)
                        context = {
                            'tooltip': 'Liste des mouvements',
                            'list_move': movements_result,
                            'form': Movement_form_filtre(),
                            'dates': date_move,
                            'title': book,
                            'list_movement': movements
                        }
                        return render(request, 'book/list_movement.html', context)
                    else:
                        messages.success(request, "vide")
                        return redirect('list_movement')
                elif type == '':
                    movements = Movement.objects.all().filter(status=1).filter(type=request.POST['date_movement'])
                    movements_result = movements
                    if movements_result:
                        movements = Movement.objects.filter(status=1)
                        context = {
                            'tooltip': 'Liste des mouvements',
                            'list_move': movements_result,
                            'form': Movement_form_filtre(),
                            'dates': date_move,
                            'title': book,
                            'list_movement': movements
                        }
                        return render(request, 'book/list_movement.html', context)
                    else:
                        messages.success(request, "vide")
                        return redirect('list_movement')
                movements = Movement.objects.all().filter(status=1).filter(type=request.POST['type'])
                movements_result = movements.filter(date_movement=request.POST['date_movement'])
                if movements_result:
                    movements = Movement.objects.filter(status=1)
                    context = {
                        'tooltip': 'Liste des mouvements',
                        'list_move': movements_result,
                        'form': Movement_form_filtre(),
                        'dates': date_move,
                        'title': book,
                        'list_movement': movements
                    }
                    return render(request, 'book/list_movement.html', context)
                else:
                    messages.success(request, "vide")
                    return redirect('list_movement')
            else:
                movements = Movement.objects.all().filter(status=1).filter(type=request.POST['type'])
                movements_result = movements.filter(book_id=request.POST['title_book']).filter(
                    date_movement=request.POST['date_movement'])
                if movements_result:
                    movements = Movement.objects.filter(status=1)
                    context = {
                        'tooltip': 'Liste des mouvements',
                        'list_move': movements_result,
                        'form': Movement_form_filtre(),
                        'dates': date_move,
                        'title': book,
                        'list_movement': movements
                    }
                    return render(request, 'book/list_movement.html', context)
                else:
                    messages.success(request, "vide")
                    return redirect('list_movement')

        else:
            movements = Movement.objects.filter(status=1)
            context = {
                'tooltip': 'Liste des mouvements',
                'list_move': movements,
                'form': Movement_form_filtre(),
                'add': change,
                'delete': delete,
                'dates': date_move,
                'title': book,
                'list_movement': movements,
                'change': change
            }
            return render(request, 'book/list_movement.html', context)
    else:
                return redirect('home_site')


@login_required(login_url='login')
def approvisionnement(request):
    if request.method == 'POST':
        id = request.POST['book'] if request.POST['book'] !='' else 0
        if id == 0:
            messages.error(request,'Veuillez selectionnez un livre')
            return redirect('approvisionnement')
        livre = Book.objects.get(pk=id)
        quantite = int(request.POST['quantite']) if request.POST['quantite'] != '' else 0
        Erreur = False
        if quantite <=0:
            messages.error(request,'La quantite doit etre superieur a zero')
            Erreur = True
        elif quantite > livre.number_copy_book:
            messages.error(request,'La quantite est insuffisante')
            Erreur = True
        if Erreur:
            return redirect('approvisionnement')

        
        livre = Book.objects.get(pk=id)
        livre.number_copy_book += quantite
        livre.save()
        forms = Movement_form({
            'book': livre,
            'quantite': quantite,
            'motif': "Approvisionnement",
            'type': 2
        })
        if forms.save():
            messages.success(request, "Approvisionnement effectué avec succès")
            return render(request, 'book/add_book.html', {'form': BookForm()})
    else:
        if request.user.is_superuser:
            book = Book.objects.filter(status=1)
        else:
            book = Book.objects.filter(status=1).filter(category__rayon__readpoint_id=request.user.readpoint.pk)
        return render(request,'book/approvisionnement.html', {
            'livre': book,
            'tooltip':'Approvisionnement'
        })


@login_required(login_url='login')
def profile_read(request, id):
    profile = ReadPoint.objects.filter(pk=id)
    for p in profile:
        read = {
            'Nom': p.name_readpoint
        }
    return render(request, 'book/profile_read.html', {'profile': read})


class ReadPointView(viewsets.ModelViewSet):
    queryset = ReadPoint.objects.all()
    serializer_class = ReadPointSerializer
    filterset_fields = ['name_readpoint']
    search_fields = ['name_readpoint', 'commune_readpoint']
    permission_classes = (IsAuthenticated,)


global cat


@login_required(login_url='login')
def transfert(request):
    if request.method == 'POST':
        print(request.POST)

        livreEnvoyer = []
        quantiteEnvoyer = []
        categorieEnvoyer = []
        qteTotal = 0
        j = 0
        nbError = 0
        # li = qi = ca = 0
        li = 0
        global yaErreur
        for bokk in request.POST:
            yaErreur = False
            if 'book' in bokk:
                if request.POST[bokk] != '' and request.POST[f'quantite{j}'] != '':
                    livreEnvoyer.append(int(request.POST[bokk]))
                    quantiteEnvoyer.append((int(request.POST[f'quantite{j}'])))
                    qteTotal += quantiteEnvoyer[j]
                    j += 1
                else:
                    nbError += 1
                    messages.error(request, f'Le {j + 1}e livre n\'est pas valide')
        if nbError > 0:
            messages.error(request, f'Il y\'a eu {nbError} erreur.s lors du transfert')
        if j == 0:
            messages.error(request,
                           f'Aucun livre n\'a été transféré\nVeuillez renseigner tous les champs puis réessayer')
            return redirect('transfert')
        if request.POST['pointlecture'] == '' or request.POST['pointlecture1'] == '':
            messages.error(request, 'Veuillez choisir le point de lecture de l\'expéditeur et du Destinateur ')
            return redirect('transfert')
        elif request.POST['pointlecture'] == request.POST['pointlecture1']:
            messages.error(request, 'Le point de lecture expéditeur ne doit pas être identique au point de lecture de '
                                    'destination')
            return redirect('transfert')
        else:
            IDpointExpediteur = request.POST['pointlecture']
            IDpointDestinateur = request.POST['pointlecture1']
        i = 0
        global tr, trans
        trans = False
        # Point de lecture de l'expediteur
        pointlectureExpediteur = ReadPoint.objects.get(pk=IDpointExpediteur)
        # Point de lecture de destination

        pointlectureDestination = ReadPoint.objects.get(pk=IDpointDestinateur)
        for iteration in livreEnvoyer:
            j -= 1
            IDlivre = iteration
            quantite = quantiteEnvoyer[i]
            # try:
            #     if not categorieEnvoyer:
            #         messages.error(request, 'Veuillez Renseigner le rayon de destination')
            #         if j <= 0:
            #             return redirect('transfert')
            #         else:
            #             continue
            #     elif categorieEnvoyer[i]:
            #         catgorie = categorieEnvoyer[i]
            # except:
            #     messages.error(request, 'Veuillez Renseigner le rayon de destination')
            #     if j <= 0:
            #         return redirect('transfert')
            #     else:
            #         continue
            i += 1
            # livre choisi
            livre = Book.objects.get(pk=IDlivre)

            if quantite > 0:
                if livre.number_copy_book < quantite:
                    messages.error(request, f'La quantité est insuffisante, échec de transfert du livre "{livre}"')
                    if j > 0:
                        continue
                    else:
                        return redirect('transfert')
            else:
                messages.error(request,
                               f'la quantité doit être supérieure à zero échec de transfert du livre "{livre}"')
                if j > 0:
                    continue
                else:
                    return redirect('transfert')
            livreExiste = Book.objects.filter(isbn_book=livre.isbn_book).filter(status=1).filter(
                category__rayon__readpoint_id=IDpointDestinateur)
            if livreExiste:
                cb = livreExiste[0].category
                livreExiste[0].number_copy_book += quantite
                livreExiste[0].save()
                livre.number_copy_book -= quantite
                if not livre.save():
                    if not trans:
                        tr = Transfert(
                            pointlectureEmetteur=IDpointExpediteur,
                            pointlectureDestinateur=IDpointDestinateur,
                            desciption=f'Transfert de {qteTotal} livres du point de'
                                       f' lecture {pointlectureExpediteur} vers le point de lecture'
                                       f' {pointlectureDestination}'
                        )
                        tr.save()
                        trans = True
                    item1 = Item_transfert(
                        livre=livreExiste[0],
                        transfert=tr,
                        quantite=quantite
                    )
                    item1.save()
                    move = Movement(
                        book=livreExiste[0],
                        motif=f'Transfert du livre "{livreExiste[0]}" du point de lecture "{pointlectureExpediteur.name_readpoint}" situe au quartier "{pointlectureExpediteur.quartier_readpoint}"'
                              f'dans la commune de "{pointlectureExpediteur.commune_readpoint}" vers le point de lecture "{pointlectureDestination.name_readpoint}"'
                              f' situe au quartier "{pointlectureDestination.quartier_readpoint}" dans la commune de "{pointlectureDestination.commune_readpoint}"',
                        type=5,
                        quantite=quantite
                    )
                    move.save()
                    messages.success(request, f'"{quantite}" exemplaire.s du livre "{livre}" est transféré avec '
                                              f'succès vers le point de lecture "{pointlectureDestination}"')
                    if j > 0:
                        continue
                    else:
                        return redirect('transfert')
                else:
                    messages.error(request,
                                   f'Échec de transfert de "{quantite}" exemplaire.s du livre "{livre}" vers le point '
                                   f'de lecture "{pointlectureDestination}"')
                    print(livre)
                    if j > 0:
                        continue
                    else:
                        return redirect('transfert')
            else:
                cb = Category.objects.filter(name_category=livre.category.name_category).filter(
                    rayon__readpoint_id=IDpointDestinateur).filter(status=1)
                if not cb:
                    messages.error(request,
                                   f'La Categorie du livre "{livre}" n\'existe pas Creation de cette categorie....')
                    rayon = Rayon.objects.filter(status=1).filter(name_rayon=livre.category.rayon.name_rayon).filter(
                        readpoint_id=IDpointDestinateur)
                    if rayon:
                        nouveauCb = Category(
                            name_category=livre.category.name_category,
                            rayon=rayon[0],
                            created_by=request.user.id
                        )
                        nouveauCb.save()
                        cat = nouveauCb
                        messages.success(request,
                                         f'La categorie "{cat}" du livre "{livre}" a été créer avec '
                                         f'succès dans le point de lecture "{cat.rayon.readpoint}"')

                    else:
                        nouveauRayon = Rayon(
                            name_rayon=livre.category.rayon.name_rayon,
                            readpoint=pointlectureDestination,
                            created_by=request.user.id,
                        )
                        nouveauRayon.save()
                        rayon = nouveauRayon
                        nouveauCb = Category(
                            name_category=livre.category.name_category,
                            rayon=rayon,
                            created_by=request.user.id
                        )
                        nouveauCb.save()
                        cat = nouveauCb
                        messages.success(request,
                                         f'La categorie "{cat}" du livre "{livre}" a été créer avec '
                                         f'succès avec son Rayon "{nouveauRayon}" dans le point de lecture "{nouveauCb.rayon.readpoint}"')
                print(cb)
                c = cat if not cb else cb[0]
                NouveauLivre = Book(
                    isbn_book=livre.isbn_book,
                    title_book=livre.title_book,
                    number_copy_book=quantite,
                    publication_date_book=livre.publication_date_book,
                    file_book=livre.file_book,
                    img1_book=livre.img1_book,
                    img2_book=livre.img2_book,
                    resume_book=livre.resume_book,
                    category=c,
                    edition_house=livre.edition_house,
                    author=livre.author
                )
                if not NouveauLivre.save():
                    if not trans:
                        tr = Transfert(
                            pointlectureEmetteur=IDpointExpediteur,
                            pointlectureDestinateur=IDpointDestinateur,
                            desciption=f'Transfert de {qteTotal} livres du point de'
                                       f' lecture {pointlectureExpediteur} vers le point de lecture'
                                       f' {pointlectureDestination}'
                        )
                        tr.save()
                        trans = True
                    messages.success(request,
                                     f'Transfert de "{quantite}" exemplaire.s du livre "{livre}" vers le point '
                                     f'de lecture "{pointlectureDestination}" réussit !')
                    item1 = Item_transfert(
                        livre=NouveauLivre,
                        transfert=tr,
                        quantite=quantite
                    )
                    item1.save()
                    move = Movement(
                        book=NouveauLivre,
                        motif=f'Transfert de "{quantite}" exemplaire.s du livre "{livre}" du point de lecture '
                              f'"{pointlectureExpediteur.name_readpoint}" situe au quartier '
                              f'"{pointlectureExpediteur.quartier_readpoint}" dans la commune de '
                              f'"{pointlectureExpediteur.commune_readpoint}" vers le point de lecture '
                              f'"{pointlectureDestination.name_readpoint}" situe au quartier '
                              f'"{pointlectureDestination.quartier_readpoint}" dans la commune de '
                              f'"{pointlectureDestination.commune_readpoint}"',
                        type=5,
                        quantite=quantite
                    )
                    move.save()

                    livre.number_copy_book -= quantite
                    livre.save()
                    move = Movement(
                        book=livre,
                        motif=f'Transfert de "{quantite}" exemplaire.s du livre "{livre}" du point de lecture '
                              f'"{pointlectureExpediteur.name_readpoint}" situe au quartier '
                              f'"{pointlectureExpediteur.quartier_readpoint}" dans la commune de '
                              f'"{pointlectureExpediteur.commune_readpoint}" vers le point de lecture '
                              f'"{pointlectureDestination.name_readpoint}" situe au quartier '
                              f'"{pointlectureDestination.quartier_readpoint}" dans la commune de '
                              f'"{pointlectureDestination.commune_readpoint}"',
                        type=5,
                        quantite=quantite
                    )
                    move.save()
                else:
                    messages.error(request, f'Échec de transfert de "{quantite}" exemplaire.s du livre "{livre}" vers '
                                            f'le point de lecture "{pointlectureDestination}"')
                    if j > 0:
                        continue
                    else:
                        return redirect('transfert')
        return redirect('transfert')
    else:
        livres = Book.objects.exclude(status=0)
        point = ReadPoint.objects.exclude(status=0)

        context = {
            'tooltip': {
                'transfert': 'Transfert des Livres',
            },
            'livres': livres,
            'point': point,

        }

        return render(request, 'book/transfert_book.html', {'context': context})


@login_required(login_url='login')
def getDataBook(request):
    # print(request.GET)
    if request.method == 'GET':
        url = int(request.GET['id'][0])
        # print(url)
        if url > 0:
            readpoint = ReadPoint.objects.get(pk=url)
            # print(readpoint)
            livre = Book.objects.exclude(status=0).filter(number_copy_book__gt=0).filter(category__rayon__readpoint=
                                                                                         readpoint)
            # print(f'livre: {json.JSONEncoder().encode(livre)}')
            tab = []
            # print(type(tab))
            for l in livre:
                tab.append(
                    {
                        'id': l.pk,
                        'isbn': l.isbn_book,
                        'titre': l.title_book,
                        'quantite': l.number_copy_book
                    })
            # print('type ', type(tab))
            print(f'tab: {tab}')
            return HttpResponse(json.JSONEncoder().encode(tab))


@login_required(login_url='login')
def getReadpoint(request):
    if request.method == 'GET':
        id_readpoint = request.GET['id']
        id_livre = request.GET['livre']
        livre = Book.objects.get(pk=id_livre)
        cat = Category.objects.filter(rayon__readpoint_id=id_readpoint).filter(
            name_category=livre.category.name_category).exclude(status=0)
        # rayons = Rayon.objects.filter(readpoint_id=id_readpoint).exclude(status=0)
        print('cat: ', cat)
        tableau = []
        for r in cat:
            tableau.append(
                {
                    'id': r.id,
                    'nom': r.name_category,
                    'rayon': f"{r.rayon.name_rayon}"
                }
            )
        return HttpResponse(json.JSONEncoder().encode(tableau))


@login_required(login_url='login')
def detailsTransfert(request, id):
    transf = Transfert.objects.get(pk=id)
    transferts = Item_transfert.objects.filter(transfert=transf)
    Emetteur = ReadPoint.objects.get(pk=transf.pointlectureEmetteur)
    Destinateur = ReadPoint.objects.get(pk=transf.pointlectureDestinateur)
    # for t in transferts:
    #     point1 = ReadPoint.objects.get(pk=t.transfert.pointlectureEmetteur)
    #     point2 = ReadPoint.objects.get(pk=t.transfert.pointlectureDestinateur)
    #     t.transfert.pointlectureEmetteur = point1
    #     t.transfert.pointlectureDestinateur = point2
    context = {
        'tooltip': 'Details du Transfert',
        'transferts': transferts,
        'Emetteur': Emetteur,
        'Destinateur': Destinateur,
        'description': transf.desciption,
        'dates': transf.dateTransfert
    }

    return render(request, 'book/detail_transfert.html', context)


@login_required(login_url='login')
def list_transfert(request):
    transferts = Transfert.objects.all()
    for t in transferts:
        point1 = ReadPoint.objects.get(pk=t.pointlectureEmetteur)
        point2 = ReadPoint.objects.get(pk=t.pointlectureDestinateur)
        t.pointlectureEmetteur = point1
        t.pointlectureDestinateur = point2
    context = {
        'tooltip': 'Liste des Transferts',
        'transferts': transferts
    }
    return render(request, 'book/list_transfert.html', {'context': context})


def example_Personne(request):
    ray = None
    if request.user.is_superuser:
        ray = Rayon.objects.filter(status=1)
    else:
        ray = Rayon.objects.filter(status=1).filter(readpoint_id=request.user.readpoint.pk).values(
            'name_rayon', 'readpoint'
        )
    titles = [
        'Rayon',
        'Point de lecture'
    ]
    print(ray)
    context = [
        ray
    ]
    ht_string = render_to_string('book/impression.html', {
        'titles': titles,
        'context': context
    })

    html_template = HTML(ht_string)
    hello = wkhtmltopdf('/add_book.html', '/media/out.pdf')

    # html_to_pdf = pdfkit.from_file(html_template)
    # print(html_to_pdf)
    # # print(html_template)
    # # print(type(html_template))
    # # html_template.write_pdf(target = 'media/impression/personne/personne.pdf')
    # # return render(request,'book/impression.html', {
    # #     'title': title,
    # #     'context': context
    # # })
    # response = HttpResponse(html_template, content_type='application/html')
    # reponse=HttpResponse(html_to_pdf, content_type='application/html')
    # reponse['Content-Disposition'] = 'attachment; filename="pdf_cv.html"'

    return PDFTemplateResponse.as_view(request, html_template)


class BookView(viewsets.ModelViewSet):
    # queryset = Book.objects.all()
    # serializer_class = ApiBook
    queryset = Category.objects.all()
    serializer_class = ApiCate
    # permission_classes = (IsAuthenticated)


class ReadPointView(viewsets.ModelViewSet):
    queryset = ReadPoint.objects.all()
    serializer_class = ApiReadPoint
    # permission_classes = (IsAuthenticated)


class Category_api_view(viewsets.ModelViewSet):
    queryset = Category.objects.values('name_category').annotate(Count('id'))
    serializer_class = Category_api





# importing the necessary libraries
from django.http import HttpResponse
from django.views.generic import View
from .process import html_to_pdf


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        # getting the template
        # changer la requette
        book = Book.objects.filter(status=1)
        # changer le chemin du temble
        pdf = html_to_pdf('book/printBook.html', {
            # on change la cle de la variable de parcours dans le templete pour la boubcle for
            "book": book,
            # le tooltip
            "title":'Liste Des Livres'
        })
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
        # rendering the template
        return HttpResponse(response, content_type='application/pdf')
    #PPRES TOUS ON CREE L'UREL POUR CETTE VIEW

class GenerateReadPointPdf(View):
        def get(self, request, *args, **kwargs):
            # getting the template
            # changer la requette
            if request.user.is_superuser:
                readPoints = ReadPoint.objects.exclude(status=0)
            else:
                readPoints = ReadPoint.objects.exclude(status=0).filter(pk=request.user.readpoint.pk)
            # changer le chemin du temble
            pdf = html_to_pdf('book/printReadPoint.html', {
                # on change la cle de la variable de parcours dans le templete pour la boubcle for
                "readPoints": readPoints,
                # le tooltip
                "title": 'Liste Des points de lecture'
            })
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
            # rendering the template
            return HttpResponse(response, content_type='application/pdf')
        # PPRES TOUS ON CREE L'UREL POUR CETTE VIEW
class GenerateRankPdf(View):
        def get(self, request, *args, **kwargs):
            # getting the template
            # changer la requette
            if request.user.is_superuser:
                list_ranks = Rayon.objects.exclude(status=0)
                form_readpoint = ReadPoint.objects.filter(status=1)
            else:
                list_ranks = Rayon.objects.exclude(status=0).filter(readpoint_id=request.user.readpoint.pk)
                form_readpoint = ReadPoint.objects.filter(status=1).filter(pk=request.user.readpoint.pk)
            # changer le chemin du temble
            pdf = html_to_pdf('book/printRank.html', {
                # on change la cle de la variable de parcours dans le templete pour la boubcle for
                "list_ranks": list_ranks,
                "form_readpoint":form_readpoint,
                # le tooltip
                "title": 'Liste Des points des rayons'
            })
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="pdf_cv.pdf"'
            # rendering the template
            return HttpResponse(response, content_type='application/pdf')
        # PPRES TOUS ON CREE L'UREL POUR CETTE VIEW