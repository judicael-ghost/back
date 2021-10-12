from rest_framework import routers
from utilisateur.views import UtilisateurAPI,getUtilisateurAPI,ProfileAPI


router = routers.DefaultRouter()

router.register('utilisateur', UtilisateurAPI, basename='utilisateur')
router.register('utilisateur/liste', getUtilisateurAPI)
router.register('utilisateur/profile', ProfileAPI)