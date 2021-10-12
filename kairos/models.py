from django.db import models


def upload_path(instance, filename):
    return '/'.join(['covers',str(instance.nom), filename])

def nameFile(instance, filename):
    return '/'.join(['images', str(instance.nom_ingredient), filename])

# Models Judicael
# Client
class Client(models.Model):
    nom = models.CharField(max_length=50, blank=False, default='')
    prenom = models.CharField(max_length=50,blank=False, default='')
    adresse = models.CharField(max_length=50,blank=False, default='')
    tel = models.CharField(max_length=50,blank=False, default='')
    point = models.CharField(max_length=50, blank=False, default='')

#Models Facture
class Facture(models.Model):
    heureFatcure = models.CharField(max_length=50, blank=False, default='')
    dateFacture = models.CharField(max_length=50, blank=False, default='')
    total = models.CharField(max_length=50, blank=False, default='')
    billet = models.CharField(max_length=50, blank=False, default='')
    rendu = models.CharField(max_length=50, blank=False, default='')

# Commmande
class CommandeClient(models.Model):
    tel = models.CharField(max_length=50, blank=False, default='')
    nom = models.CharField(max_length=50, blank=False, default='')
    prenom = models.CharField(max_length=50,blank=False, default='')
    nomPro = models.CharField(max_length=50, blank=False, default='')
    categorie = models.CharField(max_length=50, blank=False, default='')
    prix = models.CharField(max_length=50, blank=False, default='')
    quantite = models.CharField(max_length=50, blank=False, default='')
    net = models.CharField(max_length=50, blank=False, default='')
    date = models.CharField(max_length=50, blank=False, default='')


# Categorie
class Categorie(models.Model):
    nomCate = models.CharField(max_length=50, blank=False, default='')

    def __str__(self):
        return self.nomCate

# Table
class Table(models.Model):
    nom = models.CharField(max_length=50, blank=False, default='')

# Produits
class Produit(models.Model):
    nom = models.CharField(max_length=50, blank=False, default='')
    categorie = models.ForeignKey(Categorie , on_delete=models.CASCADE)
    prix = models.CharField(max_length=50, blank=False, default='')
    cover = models.FileField(blank=True, default='' , upload_to=upload_path)

    def __str__(self):
        return self.categorie.nomCate

# Commande
class Commande(models.Model):
    produit = models.CharField(max_length=50, blank=False, default='')
    nom = models.CharField(max_length=50, blank=False, default='')
    categorie = models.CharField(max_length=50, blank=False, default='')
    prix = models.CharField(max_length=50, blank=False, default='')
    quantite = models.IntegerField(blank=False, default=1)
    net = models.CharField(max_length=50, blank=False, default='')
    date = models.CharField(max_length=50, blank=False, default='')
    status = models.BooleanField(default=False, blank=True)
    facture = models.CharField(max_length=50, blank=True, default='')

# Bonus
class Bonus(models.Model):
    point = models.CharField(max_length=50, blank=False, default='')
    min = models.CharField(max_length=50, blank=False, default='')
    max = models.CharField(max_length=50, blank=False, default='')


# Model Célin
# Categorie Ingredient
class CategorieIngredient(models.Model):
    nom_categorie = models.CharField(max_length=50)
    date_ajoute = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.nom_categorie + ' ' + str(self.date_ajoute)

# Unite
class Unite(models.Model):
    nom_unite = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    date_ajoute = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
        return self.nom_unite + ' ' + str(self.symbol) + ' ' + str(self.date_ajoute)

# Lieu
class Lieu(models.Model):
    nom_lieu = models.CharField(max_length=50)
    date_ajoute = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.nom_lieu + ' ' + str(self.date_ajoute)

# Prix
class Prix(models.Model):
    prix_unitaire = models.FloatField(max_length=8)
    date_ajoute = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __int__(self):
        return self.prix_unitaire + ' ' + int(self.date_ajoute)

# Ingredient
class Ingredient(models.Model):
    nom_ingredient = models.CharField(max_length=50)
    categorie = models.ForeignKey(CategorieIngredient, on_delete=models.CASCADE,related_name="ingredient_related")
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE) #categorie_fruite_mer.ingredient_related.all()
    quantite_stock = models.FloatField(default='0', blank=True, null=True)
    #approvisionnement
    achat_lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
    achat_montant = models.FloatField(default='0', blank=True, null=True)
    achat_prix_unitaire = models.FloatField(default='0', blank=True, null=True)#Ingredient.objects.
    achat_quantite = models.FloatField(default='0', blank=True, null=True)
    achat_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    don_quantite = models.FloatField(default='0', blank=True, null=True)
    #setting quantité d'alerte
    alerte_quantite = models.FloatField(default='0', blank=True, null=True)
    date_ajoute = models.DateTimeField(auto_now_add=True, auto_now=False)
    mode = models.CharField(max_length=20,blank=True)
    image = models.ImageField(upload_to=nameFile, blank=True, null=True)
    qte_sortie= models.FloatField(default=0, null=True)

    def __str__(self):
        return self.nom_ingredient + ' ' + str(self.categorie.nom_categorie)+ ' ' + str(self.unite.nom_unite)+ ' ' + str(self.unite.symbol) + ' ' + str(self.date_ajoute) + ' ' + str(self.achat_date)


    @property
    def int_qt_don(self):
        self.don_quantite = 0
        return self.don_quantite 


    @property
    def get_quantite_total_don(self):
        quantite_total = self.quantite_stock + self.don_quantite
        return quantite_total 

    
    @property
    def get_quantite_total(self):
        quantite_total = self.quantite_stock + self.achat_quantite
        return quantite_total
    

    @property
    def get_motant_total(self):
        #total_achat = self.achat_montant + (self.achat_quantite * self.achat_prix_unitaire)
        total_achat = self.achat_quantite * self.achat_prix_unitaire
        return total_achat
    
    
    @property
    def get_mode(self):
        #total_achat = self.achat_montant + (self.achat_quantite * self.achat_prix_unitaire)
        self.mode = "creation"
        mode_post = self.mode
        return mode_post


    @property
    def int_qt_achat(self):
        self.achat_quantite = 0
        return self.achat_quantite

    @property
    def get_quantite_total_sortie(self):
        quantite_total = self.quantite_stock - self.qte_sortie
        return quantite_total

  
    def save(self,*args, **kwargs):
        if self.pk:
            if self.mode == "achat":
               self.achat_montant = self.get_motant_total
               self.quantite_stock = self.get_quantite_total
               self.achat_quantite = self.int_qt_achat
               super(Ingredient, self).save(*args, **kwargs)
            if self.mode == "don":
               self.quantite_stock = self.get_quantite_total_don
               self.don_quantite = self.int_qt_don
               super(Ingredient, self).save(*args, **kwargs) 
            else:
               super(Ingredient, self).save(*args, **kwargs)
        else:
            self.mode = "creation"
            super(Ingredient, self).save(*args, **kwargs)

# Marcher
class Marcher(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,related_name="ingredient_marchers")
    lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
    prix = models.ForeignKey(Prix, on_delete=models.CASCADE)
    date_ajoute = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.ingredient.nom_ingredient) + ' ' + str(self.lieu.nom_lieu) + ' ' + str(self.prix.prix_unitaire) + ' ' + str(self.date_ajoute)

        
# Historique
class Historique(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    categorie = models.CharField(max_length=50)
    unite = models.CharField(max_length=50)
    quantite_stock = models.FloatField(default='0', blank=True, null=True)
    achat_lieu = models.CharField(max_length=50)
    achat_montant = models.FloatField(default='0', blank=True, null=True)
    achat_prix_unitaire = models.FloatField(default='0', blank=True, null=True)
    achat_quantite = models.FloatField(default='0', blank=True, null=True)
    sortie_quantite = models.FloatField(default='0', blank=True, null=True)
    don_quantite = models.FloatField(default='0', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.ingredient.nom_ingredient


# Models Jacky
# Recette
class Recette(models.Model):
    quantite_ingredient = models.FloatField(default='1', blank=True, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unite = models.ForeignKey(Unite, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.produit.nom+ ' ' + str(self.ingredient.nom_ingredient)+ ' ' +str(self.unite.symbol)

# Models Ruffine
# Caissier
class Caissier(models.Model):
    solde = models.FloatField(default=0)
    #facture = models.ForeignKey()
    date = models.DateTimeField(auto_now=True)

# Depense
class Depense(models.Model):
    ingredient = models.CharField(max_length=50)
    prix = models.FloatField(default=0)
    quantite = models.FloatField(default=0)
    unite = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

# Kairos
class Kairos(models.Model):
    vola_kairos = models.FloatField(default=0)
    recette = models.FloatField(default=0)
    depense = models.FloatField(default=0)
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)


    @property
    def get_vola_miditra(self):
        vola_kairos = self.vola_kairos + self.recette
        return vola_kairos

    
    @property
    def get_vola_miala(self):
        vola_kairos = self.vola_kairos - self.depense
        return vola_kairos


    def save(self,*args, **kwargs):
        if self.pk:
            if self.status == True:
                self.vola_kairos = self.get_vola_miditra
                self.recette = 0
                self.depense = 0
                super(Kairos, self).save(*args, **kwargs)
            else:
                self.vola_kairos = self.get_vola_miala
                self.recette = 0
                self.depense = 0
                super(Kairos, self).save(*args, **kwargs)
        else:
            if self.status == True:
                self.vola_kairos = self.get_vola_miditra
                self.recette = 0
                self.depense = 0
                super(Kairos, self).save(*args, **kwargs)
            else:
                self.vola_kairos = self.get_vola_miala
                self.recette = 0
                self.depense = 0
                super(Kairos, self).save(*args, **kwargs)
    
