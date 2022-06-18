from django.urls import path
from rest_framework import routers

from . import views
from .views import BookView, ReadPointView, Category_api_view, example_Personne, GeneratePdf, GenerateReadPointPdf, \
    GenerateRankPdf

router = routers.DefaultRouter()
router.register('book', BookView)
router_read_point = routers.DefaultRouter()
router_read_point.register('readpoint',ReadPointView)
Category_router = routers.DefaultRouter()
Category_router.register('Category',Category_api_view)

urlpatterns = [
    path('', views.books, name="books"),
    path('add_book', views.add_book, name="add_book"),
    path('detail_book/<int:id>/', views.detail_book, name="detail_book"),
    path('readpoints/', views.read_points, name="readpoints"),
    path('readpoints/delete_read_point/<int:id>', views.delete_read_point, name="delete_read_point"),
    path('readpoints/edit_read_point/<int:id>', views.edit_read_point, name="edit_read_point"),
    path('readpoints/profile_read/<int:id>', views.profile_read, name="profile_read_point"),
    path("ranks/delete_rank/<int:id>", views.delete_rank, name="delete_rank"),
    path('ranks/', views.ranks, name="ranks"),
    path('ranks/filtre/<int:id>', views.filtrer_rank, name="filtre"),
    path('ranks/edit_rank/<int:id>', views.edit_rank, name="edit_rank"),
    path('category/', views.category, name="category"),
    path('edit_category/<int:id>/', views.edit_category, name="edit_category"),
    path('delete_category/<int:id>/', views.delete_category, name="delete_category"),
    path('author/', views.author, name="author"),
    path('edit_author/<int:id>/', views.edit_author, name="edit_author"),
    path('delete_author/<int:id>/', views.delete_author, name="delete_author"),
    path('edit-book/<int:id>/', views.edit_book, name="edit-book"),
    path('delete_book/<int:id>/', views.delete_book, name="delete_book"),
    path('movement/', views.movement, name="movement"),
    path('edit_movement/<int:id>/', views.edit_movement, name="edit_movement"),
    path('delete_movement/<int:id>/', views.delete_movement, name="delete_movement"),
    path('detail_movement/<int:id>/', views.detail_movement, name="detail_movement"),
    path('list_movement/', views.list_movement, name="list_movement"),
    path('impression_rayon/', views.example_Personne, name="impression_rayon"),
    path('approvisionnement/', views.approvisionnement, name="approvisionnement"),
    path('allbooks/', views.allbooks, name="allbooks"),
    #Transfert de livre
    path('transfert/', views.transfert, name='transfert'),
    path('getDataBook/', views.getDataBook, name='getDataBook'),
    path('detailTransfert/<int:id>/', views.detailsTransfert, name='detailTransfert'),
    path('getReadpoint/', views.getReadpoint, name='getReadpoint'),
    path('list_transfert/',views.list_transfert,name = 'list_tranfert'),
#     Pdf
    path('pdf/', GeneratePdf.as_view(),name='pdfprintBook'),
    path('pdfs/', GenerateReadPointPdf.as_view(),name='pdfprintReadPoint'),
    path('pdfRank/', GenerateRankPdf.as_view(),name='pdfprintRank'),


]
