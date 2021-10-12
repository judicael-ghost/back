from kairos.models import *
from django.contrib import admin
from kairos.models import Client

# Register your models here.

@admin.register(Client)
class Client(admin.ModelAdmin):
    list_display = ('nom', 'prenom','adresse','tel', 'point')

@admin.register(Commande)
class Commande(admin.ModelAdmin):
    list_display = ('categorie','nom', 'prix','quantite','net','date','status')

admin.site.register(Ingredient)
admin.site.register(Recette)
admin.site.register(Produit)
admin.site.register(Lieu)
admin.site.register(Prix)
admin.site.register(Marcher)
admin.site.register(CategorieIngredient)
admin.site.register(Unite)
admin.site.register(Historique)
admin.site.register(Depense)
admin.site.register(Caissier)
admin.site.register(Kairos)

