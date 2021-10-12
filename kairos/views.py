from django.db.models import Q
from django.db.models import F
from rest_framework.response import Response
from kairos.pagination import PaginationPageNumberPagination
from django.http.response import HttpResponse, JsonResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from kairos.models import Client
from kairos.serializers import *
from kairos.models import *
from rest_framework import viewsets
from rest_framework import status



class BonusViewSet(viewsets.ModelViewSet):
    queryset = Bonus.objects.all()
    serializer_class = BonusSerilazer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filterset_fields = ['id']

class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    filterset_fields = ['categorie']
    search_fields = ['categorie']

class DeleteMulti(APIView):
    def delete(self, request, cate, format=None):
        produit = Produit.objects.filter(categorie = cate)
        if produit:
            produit.delete()
            return JsonResponse({"status" : "vOfafa"} , status=status.HTTP_200_OK)
        return JsonResponse("Not found" , status=status.HTTP_404_NOT_FOUND)

class AjoutProduitViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitAddSerializer

    filterset_fields = ['categorie']
    search_fields = ['categorie']

    def post(self, request, *args, **kwargs):
        cover = request.data['cover']
        nom = request.data['nom']
        categorie = request.data['categorie']
        prix = request.data['prix']
        Produit.objects.create(nom=nom,categorie=categorie,prix=prix,cover=cover)
        return HttpResponse({'Message' : 'Produit Créée'}, status=200)

class UpdateBonustViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = BonusClientSerializer


class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    filterset_fields = ['date' , 'categorie','nom' , 'facture']


class FactureViewSet(viewsets.ModelViewSet):
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer
    filterset_fields = ['dateFacture']

class CommandeClientViewSet(viewsets.ModelViewSet):
    queryset = CommandeClient.objects.all()
    serializer_class = CommandeClientSerilazer
    filterset_fields = ['nom','tel','categorie','nomPro']

#API view Celin
#Categorie
class CategorieListe(ListAPIView):
    serializer_class = CategorieIngredientSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom_categorie']
    pagination_class = PaginationPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = CategorieIngredient.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(nom_categorie__icontains=query)
            ).distinct()
        return queryset_list

    
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CategorieIngredientSerializer(data=data)
        if serializer.is_valid():
            categorie_exsistes = CategorieIngredient.objects.filter(nom_categorie = data.get('nom_categorie')).count()
            if categorie_exsistes == 0:
                CategorieIngredient.objects.create(nom_categorie=data.get('nom_categorie'))
                return Response({'nom_categorie': data.get('nom_categorie')}, status=status.HTTP_201_CREATED)
            return Response({'message': 'categorie existe déja'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategorieSelect(APIView):

    def get(self, request):
        categories = CategorieIngredient.objects.all()
        serializer = CategorieIngredientSerializer(categories, many=True)
        return Response(serializer.data)


class CategorieDetails(APIView):

    def get_object(self, id):
        try:
            return CategorieIngredient.objects.get(id=id)

        except CategorieIngredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        categories = self.get_object(id)
        serializer = CategorieIngredientSerializer(categories)
        return Response(serializer.data)


    def put(self, request, id):
        categorie = self.get_object(id)
        data=request.data
        CategorieIngredient.objects.filter(id=categorie.id).update(nom_categorie=data.get('nom_categorie'))
        serializer = CategorieIngredientSerializer(categorie, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        categorie = self.get_object(id)
        categorie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Unite
class UniteList(APIView):

    def get(self, request):
        unites = Unite.objects.all()
        serializer = UniteSerializer(unites, many=True)
        return Response(serializer.data)


    def post(self, request):
        data=request.data
        serializer = UniteSerializer(data=data)
        if serializer.is_valid():
            unite_existes = Unite.objects.filter(nom_unite=data.get('nom_unite')).count()
            if unite_existes == 0:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': 'unites existe déja.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UniteDetails(APIView):

    def get_object(self, id):
        try:
            return Unite.objects.get(id=id)

        except Unite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        unite = self.get_object(id)
        serializer = UniteSerializer(unite)
        return Response(serializer.data)


    def put(self, request, id):
        unite = self.get_object(id)
        serializer = UniteSerializer(unite, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        unite = self.get_object(id)
        unite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

#Lieu
class LieuList(APIView):

    def get(self, request):
        lieux = Lieu.objects.all()
        serializer = LieuSerializer(lieux, many=True)
        return Response(serializer.data)


    def post(self, request):
        data=request.data
        serializer = LieuSerializer(data=data)
        if serializer.is_valid():
            lieu_existes = Lieu.objects.filter(nom_lieu= data.get('nom_lieu')).count()
            if lieu_existes == 0:
                Lieu.objects.create(nom_lieu= data.get('nom_lieu'))
                return Response({'nom_lieu': data.get('nom_lieu')}, status=status.HTTP_201_CREATED)
                #serializer.save()
            return Response({'message': 'lieu existe déja'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LieuDetails(APIView):

    def get_object(self, id):
        try:
            return Lieu.objects.get(id=id)

        except Lieu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        lieux = self.get_object(id)
        serializer = LieuSerializer(lieux)
        return Response(serializer.data)


    def put(self, request, id):
        lieu = self.get_object(id)
        serializer = LieuSerializer(lieu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        lieu = self.get_object(id)
        lieu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Prix

class PrixList(APIView):

    def get(self, request):
        prix = Prix.objects.all().order_by('prix_unitaire')
        serializer = PrixSerializer(prix, many=True)
        return Response(serializer.data)


    def post(self, request):
        data=request.data
        serializer = PrixSerializer(data=data)
        if serializer.is_valid():
            prix_existes = Prix.objects.filter(prix_unitaire=data.get('prix_unitaire')).count()
            if prix_existes == 0:
                Prix.objects.create(prix_unitaire=data.get('prix_unitaire'))
            #serializer.save()
                return Response({'prix_unitaire': data.get('prix_unitaire')}, status=status.HTTP_201_CREATED)
            return Response({'message': 'prix existe deja'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrixDetails(APIView):

    def get_object(self, id):
        try:
            return Prix.objects.get(id=id)

        except Prix.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        prix = self.get_object(id)
        serializer = PrixSerializer(prix)
        return Response(serializer.data)


    def put(self, request, id):
        unitaire = self.get_object(id)
        serializer = PrixSerializer(unitaire, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        unitaire = self.get_object(id)
        unitaire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# Celin Ingredient

class IngredientList(ListAPIView):
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nom_ingredient']
    pagination_class = PaginationPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Ingredient.objects.all().order_by('-date_ajoute')
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(nom_ingredient__icontains=query)
            ).distinct()
        return queryset_list


    def post(self, request):
        data=request.data
        print("data erreur",data)#results = Matches.objects.raw('SELECT * FROM myapp_matches GROUP BY date')
        serializer = IngredientSerializer(data=data)
        if serializer.is_valid():
            ingredient_exists = Ingredient.objects.filter(nom_ingredient=data.get('nom_ingredient')).count()
            if ingredient_exists == 0:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': 'L\'ingredient existe déja.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientAll(APIView):

    def get(self, request):
        ingredients = Ingredient.objects.all().order_by('-date_ajoute')
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)


    def post(self, request):
        data=request.data
        print("data erreur",data)#results = Matches.objects.raw('SELECT * FROM myapp_matches GROUP BY date')
        serializer = IngredientSerializer(data=data)
        if serializer.is_valid():
            ingredient_exists = Ingredient.objects.filter(nom_ingredient=data.get('nom_ingredient')).count()
            if ingredient_exists == 0:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': 'L\'ingredient existe déja.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientDetails(APIView):

    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        ingredients = self.get_object(id)
        serializer = IngredientSerializer(ingredients)
        return Response(serializer.data)


    def put(self, request, id):
        ingredient = self.get_object(id)
        data=request.data
        data['mode']="modify"
        serializer = IngredientCrudSerializer(ingredient, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        ingredient = self.get_object(id)
        #nom_historique = Ingredient.objects.get(id=ingredient.id).nom_ingredient
        ingredients_historique = Historique.objects.filter(ingredient=ingredient.id)
        ingredients_historique.delete()
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientAlert(APIView):

    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def get(self, request, id):
        ingredients = self.get_object(id)
        serializer = IngredientAlerteSerializer(ingredients)
        return Response(serializer.data)


    def put(self, request, id):
        ingredient = self.get_object(id)
        data=request.data
        data['mode']="alerte"
        serializer = IngredientAlerteSerializer(ingredient, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Approvisionnement(APIView):

    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def get(self, request, id):
        ingredients = self.get_object(id)
        serializer = ApprovisionnementSerializer(ingredients)
        return Response(serializer.data)


    def put(self, request, id):
        ingredient = self.get_object(id)
        data=request.data
        achat_unitaire = Marcher.objects.get(ingredient=ingredient.id,lieu=data['achat_lieu']).prix.prix_unitaire
        print ("Prix ",achat_unitaire)
        print("Ingredient ",Ingredient.objects.filter(id=ingredient.id).first().achat_prix_unitaire)#.update(achat_prix_unitaire=achat_unitaire)
        Ingredient.objects.filter(id=ingredient.id).update(achat_prix_unitaire=achat_unitaire)
        print("Ingredient apres",Ingredient.objects.filter(id=ingredient.id).first().achat_prix_unitaire)
        data['achat_prix_unitaire']=achat_unitaire
        data['mode']="achat"
        serializer = ApprovisionnementSerializer(ingredient, data=data)
        nom_ingredient = Ingredient.objects.get(id=ingredient.id).nom_ingredient
        categorie = Ingredient.objects.get(id=ingredient.id).categorie.nom_categorie
        unite = Ingredient.objects.get(id=ingredient.id).unite.nom_unite
        if serializer.is_valid():
            serializer.save()
            quantite_stock = Ingredient.objects.get(id=ingredient.id).quantite_stock
            print("Stock",quantite_stock)
            achat_lieu = Ingredient.objects.get(id=ingredient.id).achat_lieu.nom_lieu
            achat_montant = Ingredient.objects.get(id=ingredient.id).achat_montant
            achat_prix_unitaire = Ingredient.objects.get(id=ingredient.id).achat_prix_unitaire
            Historique.objects.create(ingredient=ingredient,categorie=categorie,unite=unite,quantite_stock=quantite_stock,achat_lieu=achat_lieu,achat_montant=achat_montant,achat_prix_unitaire=achat_prix_unitaire,achat_quantite=data['achat_quantite'])
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarcherExistence(APIView):
    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def get(self, request, id):
        ingredient = self.get_object(id)
        marcher = Marcher.objects.filter(ingredient=ingredient.id)
        serializer = MarcheSerializer(marcher, many=True)
        return Response(serializer.data)


class IngredientInssufisante(APIView):

    def get(self, request):
        ingredients = Ingredient.objects.filter(alerte_quantite__gte=F('quantite_stock')).order_by('-date_ajoute')
        #ingredients = Ingredient.objects.raw("SELECT * FROM kairos_ingredient")
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)


class IngredientStatistiqueAll(APIView):

    def get(self, request):
        ingredients = Ingredient.objects.all().order_by('-date_ajoute')
        serializer = IngredientStatistiqueSerializer(ingredients, many=True)
        return Response(serializer.data)


class IngredientStatistiqueDetails(APIView):

    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        ingredients = self.get_object(id)
        serializer = IngredientStatistiqueSerializer(ingredients)
        return Response(serializer.data)


class IngredientDon(APIView):

    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def get(self, request, id):
        ingredients = self.get_object(id)
        serializer = IngredientDonSerializer(ingredients)
        return Response(serializer.data)


    def put(self, request, id):
        ingredient = self.get_object(id)
        data=request.data
        data['mode']="don"
        serializer = IngredientDonSerializer(ingredient, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientViderStock(APIView):

    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        ingredients = self.get_object(id)
        serializer = IngredientViderSerializer(ingredients)
        return Response(serializer.data)


    def put(self, request, id):
        ingredient = self.get_object(id)
        data=request.data
        data['mode']="vider"
        data['quantite_stock']= 0
        serializer = IngredientViderSerializer(ingredient, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Marche

class MarcherList(APIView):

    def get(self, request):
        marchers = Ingredient.objects.all()
        serializer = IngredientParCMarcherSerializer(marchers, many=True)
        return Response(serializer.data)


    def post(self, request):
        data=request.data
        serializer = MarcheSerializer(data=data)
        if serializer.is_valid():
            marcher_existes = Marcher.objects.filter(ingredient = data.get('ingredient'), lieu = data.get('lieu')).count()
            if marcher_existes == 0:
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message': 'cet ingredient a deja son prix unitaire à ce lieu'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarcherDetails(APIView):

    def get_object(self, id):
        try:
            return Marcher.objects.get(id=id)

        except Marcher.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        marchers = self.get_object(id)
        serializer = MarcheSerializer(marchers)
        return Response(serializer.data)


    def put(self, request, id):
        marche = self.get_object(id)
        serializer = MarcheSerializer(marche, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        marche = self.get_object(id)
        marche.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
#Historique

class HistoriqueList(APIView):

    def get(self, request):
        historiques = Historique.objects.all().order_by('-date_created')
        serializer = HistoriqueSerializer(historiques, many=True)
        return Response(serializer.data)
    
    def delete(self, request):
        historiques = Historique.objects.all()
        historiques.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistoriqueDepenseTotale(APIView):

    def get(self, request):
        total_achat = 0
        historiques = Historique.objects.all().values('ingredient').aggregate(prix_total=Sum('achat_montant'))
        if historiques is not None:
            total_achat = historiques["prix_total"] or 0
        return Response({'depense': total_achat})




class IngredientHistory(APIView):

    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        ingredient = self.get_object(id)
        historiques = Historique.objects.filter(nom_ingredient=ingredient.nom_ingredient).order_by('-date_created')
        serializer = HistoriqueSerializer(historiques, many=True)
        return Response(serializer.data)


class IngredientPrix(APIView):

    def get_object(self, id):
        try:
            return Ingredient.objects.get(id=id)

        except Ingredient.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        ingredient = self.get_object(id)
        #historiques = Historique.objects.raw('SELECT SUM(achat_montant) as prix FROM kairos_bd_historique')
        historiques = Historique.objects.filter(nom_ingredient=ingredient.nom_ingredient).values('nom_ingredient').annotate(depence=Sum('achat_montant'))
        #serializer = HistoriqueSerializer(historiques, many=True)
        return Response(historiques)


#Jacky

class RecetteList(APIView):

    def get(self, request):
        recettes = Recette.objects.all()
        serializer = RecetteSerializer(recettes, many=True)
        return Response(serializer.data)


    def post(self, request):
        data=request.data
        serializer = RecetteSerializer(data=data)
        if serializer.is_valid():
            recette_existe = Recette.objects.filter(produit= data.get('produit'), ingredient = data.get('ingredient')).count()
            if recette_existe == 0:
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message':'ingredient est deja dans le recette de cet produit'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommandeList(APIView):

    def get(self, request):
        commandes = Commande.objects.all()
        serializer = CommandeSerializer(commandes, many=True)
        return Response(serializer.data)


    def post(self, request):
        data=request.data
        serializer = CommandeSerializer(data=data)
        if serializer.is_valid():
            produit=data['produit']
            produit_nbr=data['quantite']
            print(produit_nbr)
            ingredients_recettes =Recette.objects.filter(produit=produit)
            print("Listes des ingredient :",ingredients_recettes)
            for item in ingredients_recettes:
                print("Ingredient PAR RECCETTE:ID",item.id," Nom: ",item.ingredient.nom_ingredient," Quantite recette: ",item.quantite_ingredient)
                quantite_totale = item.quantite_ingredient * produit_nbr
                print("Ingredient PAR RECETTE:ID",item.id," Nom: ",item.ingredient.nom_ingredient," quantite totale: ", quantite_totale)
                id_ingredient = item.ingredient.id
                print("Id ingredient", id_ingredient)
                try:
                    liste_ingredient=Ingredient.objects.get(id=id_ingredient)
                    qt_stock = liste_ingredient.quantite_stock
                    print("quantite ingredient",qt_stock)
                    if qt_stock >= quantite_totale:
                        qt_ajour = qt_stock - quantite_totale
                        Ingredient.objects.get(id=id_ingredient)
                        Ingredient.objects.filter(id=id_ingredient).update(mode="sortie",qte_sortie=quantite_totale,quantite_stock=qt_ajour)
                        
                    else:
                        return Response({"IL MANQUE DES INGREDIENNT DANS LE RECETTE"},status=status.HTTP_200_OK)
                except Ingredient.DoesNotExist:
                    return Response({"message":"Ingredient not found"},status=status.HTTP_404_NOT_FOUND)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecetteDetails(APIView):

    def get_object(self, id):
        try:
            return Recette.objects.get(id=id)

        except Recette.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        recettes = self.get_object(id)
        serializer = RecetteSerializer(recettes)
        return Response(serializer.data)


    def put(self, request, id):
        recette = self.get_object(id)
        data=request.data
        serializer = RecetteSerializer(recette, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        recette = self.get_object(id)
        recette.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProduitRecette(APIView):

    def get_object(self, id):
        try:
            return Recette.objects.filter(produit=id)

        except Recette.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def get(self, request, id):
        produits = self.get_object(id)
        serializer = RecetteSerializer(produits, many=True)
        return Response(serializer.data)


# Ruffine
class CaissierListe(APIView):

 def get(self,request):
    caissiers = Caissier.objects.all()
    serializer = CaissierSerializer(caissiers, many=True)
    return Response (serializer.data)
  
 def post(self, request):
    data = request.data
    serializer = CaissierSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CaissierDetail(APIView):
    
  def get_object(self, id):
     try:
        return Caissier.objects.get(id=id)
     
     except Caissier.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)


  def get(self, request, id):
    Caissier = self.get_object(id)
    serializer = CaissierSerializer(Caissier)
    return Response(serializer.data)


  def put(self, request, id):
    caissier = self.get_object(id)
    data = request.data
    serializer = CaissierSerializer(caissier, data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self,request, id):
    caissier= self.get_object(id)
    caissier.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class DepenseListe(APIView):

  def get(self,request):
    depenses = Depense.objects.all()
    serializer = ProduitSerializer(depenses, many=True)
    return Response (serializer.data)
  
class DepenseDetail(APIView):
    
  def get_object(self, id):
     try:
        return Depense.objects.get(id=id)
     
     except Depense.DoesNotExist:
       return Response(status=status.HTTP_404_NOT_FOUND)


  def get(self, request, id):
    Depense = self.get_object(id)
    serializer = DepenseSerializer(Caissier)
    return Response(serializer.data)


  def put(self, request, id):
    depense= self.get_object(id)
    data = request.data
    serializer = DepenseSerializer(depense, data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self,request, id):
    depense= self.get_object(id)
    depense.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

