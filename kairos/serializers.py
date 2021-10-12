from rest_framework.fields import SerializerMethodField
from kairos.models import Facture
from kairos.models import Caissier, Depense
from kairos.models import Recette
from django.db.models.aggregates import Sum
from kairos.models import Client, CommandeClient,Categorie,Table, Produit, Commande, Bonus, CategorieIngredient, Historique, Ingredient, Lieu, Marcher, Prix, Unite
from rest_framework import serializers

    
class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id','nom','prenom','adresse','tel','point')

class BonusClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id','nom','prenom','adresse','tel','point')

class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = ('id','nomCate')

class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ('id','nom')

class ProduitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produit
        fields = "__all__"

class ProduitAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Produit
        fields = "__all__"

    def to_representation(self, instance):
        data =super(ProduitAddSerializer,self).to_representation(instance)
        categorie = Categorie.objects.get(id=data['categorie'])
        data['categorie'] = CategorieSerializer(categorie).data
        return data


class CommandeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commande
        fields = ('id','produit','nom','categorie','prix','quantite','net','date' , 'facture')

class CommandeClientSerilazer(serializers.ModelSerializer):

    class Meta:
        model = CommandeClient
        fields = "__all__"   

class BonusSerilazer(serializers.ModelSerializer):

    class Meta:
        model = Bonus
        fields = "__all__"   


class FactureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Facture
        fields = "__all__"


#Serializers Celin


class CategorieIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorieIngredient
        fields = '__all__'


class UniteSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Unite
        fields = '__all__'



class LieuSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Lieu
        fields = '__all__'


class PrixSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Prix
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    #image = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = Ingredient
        fields = '__all__'

    def to_representation(self, instance):
        data = super(IngredientSerializer, self).to_representation(instance)
        categorie = CategorieIngredient.objects.get(id=data['categorie'])
        unite = Unite.objects.get(id=data['unite'])
        lieu = Lieu.objects.get(id=data['achat_lieu'])
        data["categorie"] = CategorieIngredientSerializer(categorie).data
        data["unite"] = UniteSerializer(unite).data
        data["achat_lieu"] = LieuSerializer(lieu).data
        return data


class IngredientCrudSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id','nom_ingredient','categorie','unite')

    def to_representation(self, instance):
        data = super(IngredientCrudSerializer, self).to_representation(instance)
        categorie = CategorieIngredient.objects.get(id=data['categorie'])
        unite = Unite.objects.get(id=data['unite'])
        data["categorie"] = CategorieIngredientSerializer(categorie).data
        data["unite"] = UniteSerializer(unite).data
        return data


class IngredientDonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id','don_quantite','mode')


class IngredientViderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id','quantite_stock','mode')


class IngredientAlerteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id','alerte_quantite','mode')



class ApprovisionnementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ingredient
        fields= ('id',
                'achat_lieu',
                'achat_prix_unitaire',
                'achat_quantite',
                'achat_montant',
                'quantite_stock',
                'mode',
                'achat_date')

    def to_representation(self, instance):
        data = super(ApprovisionnementSerializer, self).to_representation(instance)
        lieu = Lieu.objects.get(id=data['achat_lieu'])
        data["achat_lieu"] = LieuSerializer(lieu).data
        return data


class IngredientStatistiqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'

    def to_representation(self, instance):
        data = super(IngredientStatistiqueSerializer, self).to_representation(instance)
        categorie = CategorieIngredient.objects.get(id=data['categorie'])
        unite = Unite.objects.get(id=data['unite'])
        lieu = Lieu.objects.get(id=data['achat_lieu'])
        total_achat =0
        nombre_achat =0
        achat = Historique.objects.filter(ingredient=data['id']).values('ingredient').aggregate(prix_total=Sum('achat_montant'))
        if achat is not None:
            total_achat = achat["prix_total"] or 0
        nbr_achat = Historique.objects.filter(ingredient=data['id']).count()
        if nbr_achat is not None:
            nombre_achat = nbr_achat or 0
        data["total_achat"]=total_achat
        data["nombre_achat"]=nombre_achat
        data["categorie"] = CategorieIngredientSerializer(categorie).data
        data["unite"] = UniteSerializer(unite).data
        data["achat_lieu"] = LieuSerializer(lieu).data
        return data



class MarcheSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Marcher
        fields = '__all__'

    def to_representation(self, instance):
        data = super(MarcheSerializer, self).to_representation(instance)
        ingredient = Ingredient.objects.get(id=data['ingredient'])
        lieu = Lieu.objects.get(id=data['lieu'])
        prix = Prix.objects.get(id=data['prix'])
        data["ingredient"] = IngredientSerializer(ingredient).data
        data["lieu"] = LieuSerializer(lieu).data
        data["prix"] = PrixSerializer(prix).data
        return data


class IngredientParCMarcherSerializer(serializers.ModelSerializer):
    ingredient_marchers = SerializerMethodField('get_marcer')
    class Meta:
        model = Ingredient
        fields = '__all__'

    def get_marcer(self, id):
        marchers = Marcher.objects.filter(ingredient=id)
        return MarcheSerializer(marchers, many=True).data


    def to_representation(self, instance):
        data = super(IngredientParCMarcherSerializer, self).to_representation(instance)
        categorie = CategorieIngredient.objects.get(id=data['categorie'])
        unite = Unite.objects.get(id=data['unite'])
        data["categorie"] = CategorieIngredientSerializer(categorie).data
        data["unite"] = UniteSerializer(unite).data
        return data


class HistoriqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Historique
        fields = '__all__' 

    def to_representation(self, instance):
        data = super(HistoriqueSerializer, self).to_representation(instance)
        ingredient = Ingredient.objects.get(id=data['ingredient'])
        data["ingredient"] = IngredientSerializer(ingredient).data
        return data


#Jacky

class RecetteSerializer(serializers.ModelSerializer):
    class Meta:
        model =Recette
        fields = '__all__'

    def to_representation(self, instance):
        data = super(RecetteSerializer, self).to_representation(instance)
        produit = Produit.objects.get(id=data['produit'])
        ingredient = Ingredient.objects.get(id=data['ingredient'])
        unite = Unite.objects.get(id=data['unite'])
        data["produit"] = ProduitSerializer(produit).data
        data["ingredient"] = IngredientSerializer(ingredient).data
        data["unite"] = UniteSerializer(unite).data
        return data

# Ruffine

class CaissierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caissier
        fields = '__all__'


class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = '__all__'