from django.contrib import admin
from .models import Stock,Category
from .forms import StockCreateForm

#To change the display of the stock elements in the admin page. Not in my notes.
class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['category', 'item_name', 'issue_by', 'quantity']#To manage what attributes of the model element must be displayed.
    form = StockCreateForm#To tell the admin page to use the StockCreateForm model for entering data for this model(Stock).
    list_filter = ['category']#To show the filter pannel in the admin page
    search_fields = ['category', 'item_name']#To manage which attributes are used to filter the search here: category or item_name
    
# Register your models here.
admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
