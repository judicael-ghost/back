from django.db import models
from django.contrib.auth.models import User

def upload_path(instance, filename):
    return '/'.join(['covers', str(instance.type), filename])

class UtilisateurProfil(models.Model):
    accounts = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    telephone = models.CharField(max_length=13)
    image = models.FileField(blank=True, default='', upload_to=upload_path)
    