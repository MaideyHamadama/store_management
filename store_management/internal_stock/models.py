from django.db import models
from providers.models import Provider
# Create your models here.

class Stock(models.Model):
    reference = models.CharField(max_length=50, unique=True, blank=False, null=False)
    provider = models.ForeignKey(Provider, verbose_name = "Provider", on_delete=models.CASCADE, blank=False, null=True)
    item_name = models.CharField(verbose_name = "article", max_length=50, blank=False, null=False, unique=True)
    quantity = models.PositiveIntegerField(verbose_name = "quantite", default='0', blank=True, null=True)
    receive_quantity = models.PositiveIntegerField(verbose_name = "quantite recu", default='0', blank=True, null=True)
    receive_by = models.CharField(verbose_name = "recu par", max_length=50, blank=True, null=True)
    issue_quantity = models.PositiveIntegerField(verbose_name = "quantite emise", default='0', blank=True, null=True)
    issue_by = models.CharField(verbose_name = "emis par", max_length=50, blank=True, null=True)
    issue_to = models.CharField(verbose_name = 'emis a', max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.PositiveIntegerField(verbose_name='Niveau seuil',default='0', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    observations = models.CharField(max_length=250, blank=True, null=True)
    material_status = models.BooleanField(verbose_name='Material Defectuous',blank=True, null=True, default=False)
    back_to_usine = models.BooleanField(verbose_name = "retour en usine", blank=True, null=True)
    
    def __str__(self):
        return self.item_name
    
class StockHistory(models.Model):
    reference = models.CharField(max_length=50,blank=False, null=False)    
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=9, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    observations = models.CharField(max_length=250, blank=True, null=True)
    material_status = models.BooleanField(verbose_name='Material Defectuous',blank=True, null=True, default=False)
    back_to_usine = models.BooleanField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Stock Histories"