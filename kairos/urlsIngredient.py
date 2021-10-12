from django.urls import path
from kairos.views import *



urlpatterns = [
    # Celin
    path('categories/', CategorieListe.as_view()),
    path('categories/<int:id>/', CategorieDetails.as_view()),
    path('categoriesselect/', CategorieSelect.as_view()),
    path('historiques/', HistoriqueList.as_view()),
    path('historiques/<int:id>/', IngredientHistory.as_view()),
    path('totaldepense/', HistoriqueDepenseTotale.as_view()),
    path('statistique/<int:id>/', IngredientPrix.as_view()),
    path('ingredients/', IngredientList.as_view()),
    path('ingredients/<int:id>/', IngredientDetails.as_view()),
    path('ingredients/<int:id>/parametre/', IngredientAlert.as_view()),
    path('ingredients/<int:id>/aprovisionnement/', Approvisionnement.as_view()),
    path('ingredients/<int:id>/don/', IngredientDon.as_view()),
    path('ingredients/<int:id>/vider/', IngredientViderStock.as_view()),
    path('ingredients/<int:id>/trouver', MarcherExistence.as_view()),
    path('ingredientsInssufisante/', IngredientInssufisante.as_view()),
    path('ingredientsliste/', IngredientAll.as_view()),
    path('statistiques/', IngredientStatistiqueAll.as_view()),
    path('statistiques/<int:id>/', IngredientStatistiqueDetails.as_view()),
    path('lieux/', LieuList.as_view()),
    path('lieux/<int:id>/', LieuDetails.as_view()),
    path('marchers/', MarcherList.as_view()),
    path('marchers/<int:id>/', MarcherDetails.as_view()),
    path('prix/', PrixList.as_view()),
    path('prix/<int:id>/', PrixDetails.as_view()),
    path('unites/', UniteList.as_view()),
    path('unites/<int:id>/', UniteDetails.as_view()),

    #Jacky
    path('produiterecette/<int:id>', ProduitRecette.as_view()),
    path('recettes/', RecetteList.as_view()),
    path('recettes/<int:id>/', RecetteDetails.as_view()),
    path('ingredientmoins', CommandeList.as_view()),

    # Ruffine
    path('caissiers', CaissierListe.as_view()),
    path('caissiers/<int:id>', CaissierDetail.as_view()),
    path('depenses/<int:id>', DepenseDetail.as_view()),
    path('depenses', DepenseListe.as_view()),

]
