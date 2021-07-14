from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages#Use for notifcation instead of using javascript
from django.contrib.auth.decorators import login_required
from .models import *
from internal_stock.models import Stock as internal_stock
from providers.models import Provider
from .forms import *
import csv

store_name = "Yassa"

#Function return if user is a store keeper
def isStoreKeeper(user):
    return user.groups.filter(name="Store_keeper").exists()

#Function return if user is a clientProviderMember group
def isClientProviderMember(user):
    return user.groups.filter(name="client_provider_member").exists()

# Create your views here.

def home(request):
    title = "Welcome: This is the home page"
    context = {
        "title" : title
    }
    return redirect("/yassa/list_items")
    return render(request, "store/home.html", context)

@login_required
def list_items(request):
    global store_name
    storeKeeperMember = isStoreKeeper(request.user)
    clientProviderMember = isClientProviderMember(request.user)
    title = 'List of Items'
    tests = []
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all().order_by('-last_updated')
    for instance in queryset:
        reorder = instance.reorder_level
        reorder_min_critical = reorder*0.2
        provider = Provider.objects.filter(id=instance.provider_id).values()
        provider_name = ""
        for pro in provider:
            provider_name = pro['first_name'] + " " + pro['name']
        tests.append([instance, int(reorder_min_critical), provider_name])
    context = {
        "header" : title,
        "title" : store_name,
        "store_name" : store_name,
        "queryset" : queryset,
        "form" : form,
        "instance_and_maxReorder" : tests,
        "storeKeeperMember" : storeKeeperMember,
        "clientProviderMember" : clientProviderMember,
    }
    #To create an automatic search on the model stock, instead of using AJAX
    if request.method == 'POST':
        tests = []
        queryset = Stock.objects.filter(
            item_name__icontains=form['article'].value()
        ).order_by('-last_updated')
        for instance in queryset:
            reorder = instance.reorder_level
            reorder_min_critical = reorder*0.2
            provider = Provider.objects.filter(id=instance.provider_id).values()
            provider_name = ""
            for pro in provider:
                provider_name = pro['first_name'] + " " + pro['name']
            tests.append([instance, int(reorder_min_critical), provider_name]) 

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of items in yassa stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['ITEM NAME', 'QUANTITY', 'REORDER LEVEL', 'ISSUE BY', 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.item_name, stock.quantity, stock.reorder_level, stock.issue_by, stock.last_updated])
            return response
        
        context = {
            "form" : form,
            "title" : store_name,
            "store_name" : store_name,
            "header" : title,
            "instance_and_maxReorder" : tests,
            "storeKeeperMember" : storeKeeperMember,
            "clientProviderMember" : clientProviderMember,
        }
    return render(request, "store/list_items.html", context)

@login_required
def add_items(request):
    global store_name
    clientProviderMember = isClientProviderMember(request.user)
    form = StockCreateForm(request.POST or None)
    title = "Add an item in the store"
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully Saved")
        return redirect('/yassa/list_items')
    context = {
        "form" : form,
        "store_name" : store_name,
        "title" : title,
        "clientProviderMember" : clientProviderMember,
    }
    return render(request, "store/add_items.html", context)

@login_required
def update_items(request, pk):
    global store_name
    clientProviderMember = isClientProviderMember(request.user)
    queryset = Stock.objects.get(id=pk)
    internal_queryset = internal_stock.objects.all()
    #Check if the item exist in the internal stock
    if internal_queryset.filter(item_name=queryset.item_name).exists():
        internal_stock_item = internal_stock.objects.get(item_name=queryset.item_name)
    else:
        internal_stock_item = None
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            #change the item name in the internal stock
            if internal_stock_item:
                instance = form.save(commit=False)
                internal_stock_item.item_name = instance.item_name
                internal_stock_item.save()
                instance.save()
            form.save()
        messages.success(request, "Successfully Updated")
        return redirect('/yassa/list_items')
    context = {
        'form' : form,
        'store_name' : store_name,
        "clientProviderMember" : clientProviderMember,
    }
    return render(request, 'store/add_items.html', context)

@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/')
    return render(request, 'store/delete_items.html')

@login_required
def stock_detail(request, pk):
    global store_name
    clientProviderMember = isClientProviderMember(request.user)
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset" : queryset,
        "store_name" : store_name,
        "clientProviderMember" : clientProviderMember,
    }
    return render(request, "store/stock_detail.html", context)

@login_required
def issue_items(request, pk):
    global store_name
    clientProviderMember = isClientProviderMember(request.user)
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
        add_to_other_stock = instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued successfully, " + str(instance.quantity) + " " + str(instance.item_name) + "s now left in Store")
        instance.issue_to = "internal"
        queryset = Stock.objects.get(id=pk)
        #To add to the internal stock
        if instance.issue_to == 'internal':
            yassa_stock_item_name = queryset.item_name
            yassa_stock_reference = queryset.reference
            #if item_name doesn't exist in the internal store database, we create it.
            try:
                queryset_internal_store = internal_stock.objects.get(item_name=yassa_stock_item_name)
            except internal_stock.DoesNotExist:
                internal_stock.objects.create(item_name=yassa_stock_item_name,issue_by="Yassa", reference=yassa_stock_reference)                
                queryset_internal_store = internal_stock.objects.get(item_name=yassa_stock_item_name)
            queryset_internal_store.issue_quantity = 0
            queryset_internal_store.quantity += add_to_other_stock
            queryset_internal_store.issue_by = "Yassa"
            queryset_internal_store.receive_quantity = add_to_other_stock
            queryset_internal_store.receive_by = None
            queryset_internal_store.observations = instance.observations
            #Pull the trigger for the receiving store
            queryset_internal_store.save()
        instance.save()            
        return redirect('/yassa/stock_detail/' + str(instance.id))
    context = {
        "title" : 'Issue ' + str(queryset.item_name),
        "queryset" : queryset,
        "form" : form,
        "store_name" : store_name,
        "username" : 'Issue By ' + str(request.user),
        "clientProviderMember" : clientProviderMember,
    }
    
    return render(request, "store/add_items.html", context)

@login_required
def receive_items(request, pk):
    global store_name
    clientProviderMember = isClientProviderMember(request.user)
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.receive_by = str(request.user)
        instance.save()
        messages.success(request, "Received successfully, " + str(instance.quantity) + " " + str(instance.item_name) + "s now in store")
        return redirect('/yassa/stock_detail/' + str(instance.id))
    context = {
        "title" : "Receive " + str(queryset.item_name),
        "instance" : queryset,
        "form" : form,
        "store_name" : store_name,
        "username" : 'Receive By : ' + str(request.user),
        "clientProviderMember" : clientProviderMember,
    }
    return render(request, "store/add_items.html", context)

@login_required
def reorder_level(request, pk):
    global store_name
    clientProviderMember = isClientProviderMember(request.user)
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance = queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(instance.reorder_level))
        return redirect("/yassa/list_items")
    context = {
        "instance" : queryset,
        "form" : form,
        "store_name" : store_name,
        "clientProviderMember" : clientProviderMember,
    }
    
    return render(request, "store/add_items.html", context)

@login_required
def list_history(request):
    global store_name
    clientProviderMember = isClientProviderMember(request.user)
    header = 'HISTORY OF ITEMS'
    queryset = StockHistory.objects.all().order_by('-last_updated')
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "form" : form,
        "header" : header,
        "store_name" : store_name,
        "queryset" : queryset,
        "clientProviderMember" : clientProviderMember,
    }
    if request.method == 'POST':
        
        if form['start_date'].value() and form['end_date'].value():
            queryset = StockHistory.objects.filter(
                item_name__icontains=form['article'].value(),
                last_updated__range=[
                    form['start_date'].value(),
                    form['end_date'].value()
                ]
            ).order_by('-last_updated')
        else:
            queryset = StockHistory.objects.filter(
                item_name__icontains = form['article'].value()
            ).order_by('-last_updated')
        
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="Yassa Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(['ITEM NAME', 'REFERENCE', 'QUANTITY', 'ISSUE QUANTITY', 'RECEIVE QUANTITY', 'RECEIVE BY', 'ISSUE BY', 'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.item_name,
                     stock.reference,
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
            "store_name" : store_name,
            "queryset" : queryset,
            "clientProviderMember" : clientProviderMember,
        }
    return render(request, "store/list_history.html", context)
    