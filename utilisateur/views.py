from rest_framework import viewsets
from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from utilisateur.serializers import ProfileSerializers, UtilisateurSerializers
from utilisateur.models import UtilisateurProfil



class UtilisateurAPI(viewsets.ViewSet):
    def list(self, request):
        user = User.objects.get(username=request.user)
        user_data = UtilisateurSerializers(user).data
        return Response(user_data)

class ProfileAPI(viewsets.ModelViewSet):
    queryset = UtilisateurProfil.objects.all()
    serializer_class = ProfileSerializers
    
class getUtilisateurAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UtilisateurSerializers
