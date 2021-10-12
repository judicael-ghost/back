from rest_framework import routers
from kairos import views
from kairos.views import *

router = routers.DefaultRouter()
router.register('clients', views.ClientViewSet)
router.register('categorie',views.CategorieViewSet)
router.register('tables',views.TableViewSet)
router.register('produits',views.ProduitViewSet)
router.register('ajoutproduits',views.AjoutProduitViewSet)
router.register('commandes',views.CommandeViewSet)
router.register('commandesClient',views.CommandeClientViewSet)
router.register('bonus',views.BonusViewSet)
router.register('update',views.UpdateBonustViewSet)
router.register('factures',views.FactureViewSet)

