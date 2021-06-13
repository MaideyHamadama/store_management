from django.db import models
from django.core.validators import RegexValidator
#from internal_stock.models import Stock
#from store.models import Stock as YassaStock
# Create your models here.
class Provider(models.Model):
    
    class Meta:
        verbose_name_plural = "Providers"
        
    first_name = models.CharField(verbose_name = 'prenoms', max_length=50, blank=True, null=False)
    name = models.CharField(verbose_name = 'noms', max_length=50, blank=True, null=False)
    tax_registration_number = models.CharField(verbose_name = 'matricule fiscale', max_length=50, blank=True, null=False, unique=True)
    society = models.CharField(verbose_name = 'societe', max_length=50, blank=True, null=False)
    telephone = models.CharField(max_length=9, blank=True, null=True, unique=True, validators=[RegexValidator(r"6[9|7|6|5|2]\d{7}","This field is incorrect")])
    fax = models.CharField(max_length=50, blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=9, blank=True, null=True, unique=True, validators=[RegexValidator(r"6[9|7|6|5|2]\d{7}","This field is incorrect")])
    email = models.EmailField(max_length=50, blank=True, null=False, unique=True)
    adresse = models.CharField(max_length=50, blank=True, null=False)
    
    def __str__(self):
        return (self.first_name + " " + self.name)
      
class Invoice(models.Model):        
    class Meta:
        verbose_name_plural = "Invoices"
    
    provider = models.ForeignKey(Provider, verbose_name = 'fournisseur', on_delete=models.CASCADE)
    #internal_stock = models.ForeignKey(Stock, verbose_name = 'stock interne', on_delete=models.CASCADE, blank=True, null=True, )
    #yassa_stock = models.ForeignKey(YassaStock, verbose_name = 'stock yassa', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0,verbose_name = 'quantite')
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    total_ht = models.PositiveBigIntegerField(default=0,blank=False, null=False)
    total_tva = models.PositiveBigIntegerField(default=0,blank=False, null=False)
    total_ttc = models.PositiveBigIntegerField(default=0,blank=False, null=False)