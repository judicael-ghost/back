from utilisateur.models import UtilisateurProfil
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class UtilisateurProfilInline(admin.StackedInline):
    model = UtilisateurProfil

class UtilisateurAdmin(UserAdmin):
    inlines = (UtilisateurProfilInline, ) 

admin.site.unregister(User)
admin.site.register(User, UtilisateurAdmin)
admin.site.register(UtilisateurProfil)