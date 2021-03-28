from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages#Use for notifcation instead of using javascript
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
import csv
# Create your views here.

def home(request):
    title = "Welcome: This is the home page"
    context = {
        "title" : title
    }
    return redirect("/list_items")
    #return render(request, "store/home.html", context)

@login_required
def list_items(request):
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
    }
    #To create an automatic search on the model stock, instead of using AJAX
    if request.method == 'POST':
        tests = []
        category = form['category'].value()
        queryset = Stock.objects.filter(
            item_name__icontains=form['item_name'].value()
        )
        if (category != ''):
            queryset = queryset.filter(category_id=category)
        
        for instance in queryset:
            print(instance)
            reorder = instance.reorder_level
            reorder_min_critical = reorder*0.2
            tests.append([instance, int(reorder_min_critical)])

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
            "instance_and_maxReorder" : tests,
        }
    return render(request, "store/list_items.html", context)

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
    return render(request, "store/add_items.html", context)

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
    return render(request, 'store/add_items.html', context)

@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/list_items')
    return render(request, 'store/delete_items.html')

@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset" : queryset,
    }
    return render(request, "store/stock_detail.html", context)

@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
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

@login_required
def receive_items(request, pk):
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
    }
    return render(request, "store/add_items.html", context)

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
    
    return render(request, "store/add_items.html", context)

@login_required
def list_history(request):
    header = 'HISTORY OF ITEMS'
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "form" : form,
        "header" : header,
        "queryset" : queryset,
    }
    if request.method == 'POST':
        category = form['category'].value()
        queryset = StockHistory.objects.filter(
            item_name__icontains=form['item_name'].value(),
            last_updated__range=[
                form['start_date'].value(),
                form['end_date'].value()
            ]
        )
        if (category != ''):
            queryset = queryset.filter(category_id=category)
        
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY','ITEM NAME', 'QUANTITY', 'ISSUE QUANTITY', 'RECEIVE QUANTITY', 'RECEIVE BY', 'ISSUE BY', 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.category,
                     stock.item_name,
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
        }
    return render(request, "store/list_history.html", context)
    