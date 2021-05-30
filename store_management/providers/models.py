from django.db import models
from django.core.validators import RegexValidator
from internal_stock.models import Stock
from store.models import Stock as YassaStock
# Create your models here.
class Provider(models.Model):
    
    class Meta:
        verbose_name_plural = "Providers"
        
    first_name = models.CharField(max_length=50, blank=True, null=False)
    name = models.CharField(max_length=50, blank=True, null=False)
    tax_registration_number = models.CharField(max_length=50, blank=True, null=False, unique=True)
    society = models.CharField(max_length=50, blank=True, null=False)
    telephone = models.CharField(max_length=9, blank=True, null=True, unique=True, validators=[RegexValidator(r"6\d{8}","This field is incorrect")])
    fax = models.CharField(max_length=50, blank=True, null=True, unique=True)
    mobile = models.CharField(max_length=9, blank=True, null=True, unique=True, validators=[RegexValidator(r"6\d{8}","This field is incorrect")])
    email = models.EmailField(max_length=50, blank=True, null=False, unique=True)
    adresse = models.CharField(max_length=50, blank=True, null=False)
    
    def __str__(self):
        return (self.tax_registration_number)
      
class Invoice(models.Model):        
    class Meta:
        verbose_name_plural = "Invoices"
    
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    internal_stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, null=True, )
    yassa_stock = models.ForeignKey(YassaStock, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0,)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    total_ht = models.PositiveBigIntegerField(blank=True, null=False)
    total_tva = models.PositiveBigIntegerField( blank=True, null=False)
    total_ttc = models.PositiveBigIntegerField( blank=True, null=False)