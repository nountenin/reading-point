from django.urls import path
from borrow.views import *

urlpatterns = [
    path('', borrow, name="borrows"),
    path('addborrow/', add_borrows, name="add-borrow"),
    path('editborrow/<int:id>/', edit_borrow, name="edit_borrow"),
    path('delete_borrow/<int:id>/', delete_borrow, name="delete_borrow"),
    path('returns/<int:id>/', returns, name="returns"),
    path('liste_borrow_return/',liste_borrow_return , name="liste_borrow_return"),
    path('changeBorrowStatus/<int:id>/', changeBorrowStatus, name="changeBorrowStatus"),
    path('retour/', retour, name="retour"),
    path('parametre/', parametre, name="parametre"),
    path('pdf/', GeneratePdf.as_view(), name='pdfprintBorrow'),
    path('pdfs/', GenerateRetourPdf.as_view(), name='pdfprintBorrowRetour'),
]
