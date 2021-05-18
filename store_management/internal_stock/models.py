from django.db import models

# Create your models here.

class Stock(models.Model):
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
    date_created = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    observations = models.CharField(max_length=250, blank=True, null=True)
    material_status = models.BooleanField(verbose_name='Material defectuous',blank=True, null=True, default=False)
    back_to_usine = models.BooleanField(blank=True, null=True)
    
    def __str__(self):
        return self.item_name + ' ' + str(self.quantity)
    
class StockHistory(models.Model):
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
    material_status = models.BooleanField(verbose_name='materials_status',blank=True, null=True)
    back_to_usine = models.BooleanField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Stock Histories"