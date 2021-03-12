from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages#Use for notifcation instead of using javascript
from .models import Stock
from .forms import *
import csv
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
        queryset = Stock.objects.filter(#category__icontains=form['category'].value(),
                                        #item_name__icontains=form['item_name'].value()
                                        )
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.category, stock.item_name, stock.quantity])
            return response
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
        messages.success(request, "Successfully Saved")
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
            messages.success(request, "Successfully Updated")
            return redirect('/list_items')
        
    context = {
        'form' : form
    }
    return render(request, 'store/add_items.html', context)

def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/list_items')
    return render(request, 'store/delete_items.html')

def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset" : queryset,
    }
    return render(request, "store/stock_detail.html", context)

def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued successfully, " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()
        return redirect('/stock_detail/' + str(instance.id))
    context = {
        "title" : 'Issue ' + str(queryset.item_name),
        "queryset" : queryset,
        "form" : form,
        "username" : 'Issue By ' + str(request.user),
    }
    
    return render(request, "store/add_items.html", context)

def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received successfully, " + str(instance.quantity) + " " + str(instance.item_name) + "s now in store")
        return redirect('/stock_detail/' + str(instance.id))
    context = {
        "title" : "Receive " + str(queryset.item_name),
        "instance" : queryset,
        "form" : form,
        "username" : 'Receive By : ' + str(request.user),
    }
    return render(request, "store/add_items.html", context)