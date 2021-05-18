from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages#Use for notifcation instead of using javascript
from django.contrib.auth.decorators import login_required
from .models import Stock
from store.models import Stock as yassa_stock
from .forms import *
import csv
# Create your views here.
store_name = "Internal Stock"

def home(request):
    title = "Welcome: This is the internal stock page"
    global store_name
    context = {
        "title" : title,
        "store_name" : store_name
    }
    return redirect("/list_items")
    return render(request, "internal_stock/home.html", context)

@login_required
def list_items(request):
    global store_name
    title = 'List of Items'
    tests = []
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()
    for instance in queryset:
        reorder = instance.reorder_level
        reorder_min_critical = reorder*0.2
        tests.append([instance, int(reorder_min_critical)])
    
    context = {
        "header" : title,
        "queryset" : queryset,
        "form" : form,
        "instance_and_maxReorder" : tests,
        "store_name" : store_name
    }
    #To create an automatic search on the model stock, instead of using AJAX
    if request.method == 'POST':
        tests = []
        queryset = Stock.objects.filter(
            item_name__icontains=form['item_name'].value()
        )        
        for instance in queryset:
            print(instance)
            reorder = instance.reorder_level
            reorder_min_critical = reorder*0.2
            tests.append([instance, int(reorder_min_critical)])

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.item_name, stock.quantity])
            return response
        
        context = {
            "form" : form,
            "header" : title,
            "instance_and_maxReorder" : tests,
        }
    return render(request, "internal_stock/list_items.html", context)

@login_required
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
    return render(request, "internal_stock/add_items.html", context)

@login_required
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
    return render(request, 'internal_stock/add_items.html', context)

@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/list_items')
    return render(request, 'internal_stock/delete_items.html')

@login_required
def stock_detail(request, pk):
    global store_name
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset" : queryset,
        "store_name" : store_name
    }
    return render(request, "internal_stock/stock_detail.html", context)

@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance = queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))
        return redirect("/list_items")
    context = {
        "instance" : queryset,
        "form" : form,
    }
    
    return render(request, "internal_stock/add_items.html", context)

@login_required
def issue_items(request, pk):
    global store_name
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        #Check if issue quantity is greater than quantity to avoid negative quantity in the stock
        if instance.issue_quantity > instance.quantity:
            messages.warning(request, "The issue quantity " + str(instance.issue_quantity) + " is above the stock quantity.")
            return redirect('/stock_detail/' + str(instance.id))
        instance.quantity -= instance.issue_quantity
        add_to_other_stock = instance.issue_quantity#To add to other stores of the stock
        instance.issue_by = str(request.user)
        messages.success(request, "Issued successfully, " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.save()
        queryset = Stock.objects.get(id=pk)
        #To add to yassa stock
        if queryset.issue_to == 'yassa':
            internal_stock_item_name = queryset.item_name
            queryset_yassa = yassa_stock.objects.get(item_name=internal_stock_item_name)
            queryset_yassa.quantity += add_to_other_stock
            queryset_yassa.issue_by = "Internal Stock"
            queryset_yassa.receive_quantity = add_to_other_stock
            #Pull the trigger for the receiving stock
            queryset_yassa.issue_quantity = 0
            queryset_yassa.save()
            print(queryset_yassa)
        return redirect('/stock_detail/' + str(instance.id))
    context = {
        "title" : 'Issue ' + str(queryset.item_name),
        "queryset" : queryset,
        "form" : form,
        "username" : 'Issue By ' + str(request.user),
        "store_name" : store_name
    }
    
    return render(request, "internal_stock/add_items.html", context)

@login_required
def receive_items(request, pk):
    global store_name
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Received successfully, " + str(instance.quantity) + " " + str(instance.item_name) + "s now in store")
        return redirect('/stock_detail/' + str(instance.id))
    context = {
        "title" : "Receive " + str(queryset.item_name),
        "instance" : queryset,
        "form" : form,
        "username" : 'Receive By : ' + str(request.user),
        "store_name" : store_name
    }
    return render(request, "internal_stock/add_items.html", context)

@login_required
def list_history(request):
    global store_name
    header = 'HISTORY OF ITEMS'
    queryset = StockHistory.objects.all().order_by('-last_updated')
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "form" : form,
        "header" : header,
        "queryset" : queryset,
        "store_name" : store_name,
    }
    if request.method == 'POST':
        queryset = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value(),
        ).order_by('-last_updated')
        
        #To save csv file
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(['ITEM NAME', 'QUANTITY', 'ISSUE QUANTITY', 'RECEIVE QUANTITY', 'RECEIVE BY', 'ISSUE BY', 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.item_name,
                     stock.quantity,
                     stock.issue_quantity,
                     stock.receive_quantity,
                     stock.receive_by,
                     stock.issue_by,
                     stock.last_updated]
                )
            return  response
        
        context = {
            "form" : form,
            "header" : header,
            "queryset" : queryset,
            "store_name" : store_name,
        }
    return render(request, "internal_stock/list_history.html", context)
    