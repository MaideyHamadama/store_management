from django.contrib import admin
from .models import Stock
from .forms import StockCreateForm

#To change the display of the stock elements in the admin page. Not in my notes.
class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'issue_by', 'quantity']#To manage what attributes of the model element must be displayed.
    form = StockCreateForm#To tell the admin page to use the StockCreateForm model for entering data for this model(Stock).
    search_fields = ['item_name']#To manage which attributes are used to filter the search here: category or item_name
    
# Register your models here.
admin.site.register(Stock, StockCreateAdmin)
