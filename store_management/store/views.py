from django.shortcuts import render,redirect
from .models import Stock
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm
# Create your views here.

def home(request):
    title = "Welcome: This is the home page"
    context = {
        "title" : title
    }
    return render(request, "store/home.html", context)

def list_items(request):
    title = 'List of Items'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    context = {
        "header" : title,
        "queryset" : queryset,
        "form" : form
    }
    #To create an automatic search on the model stock, instead of using AJAX
    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),item_name__icontains=form['item_name'].value())
        context = {
            "form" : form,
            "header" : title,
            "queryset" : queryset,
        }
    return render(request, "store/list_items.html", context)

def add_items(request):
    form = StockCreateForm(request.POST or None)
    title = "Add an item in the store"
    if form.is_valid():
        form.save()
        return redirect('/list_items')
    context = {
        "form" : form,
        "title" : title,
    }
    return render(request, "store/add_items.html", context)

def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            #return redirect('/list_items')
        
    context = {
        'form' : form
    }
    return render(request, 'store/add_items.html', context)

def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == "POST":
        queryset.delete()
        return redirect('/list_items')
    return render(request, 'store/delete_items.html')