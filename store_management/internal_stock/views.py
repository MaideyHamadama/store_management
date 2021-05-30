from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages#Use for notifcation instead of using javascript
from django.contrib.auth.decorators import login_required
from .models import Stock as internal_stock
from store.models import Stock as yassa_stock
from clients.models import Receipt
from providers.models import Invoice,Provider
from clients.models import Client
from .forms import *
import csv
#For pdf file generation
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
#custom decorator
from .decorators import is_not_superuser

store_name = "Internal Stock"

#Function return if user is a store keeper
def isStoreKeeper(user):
    return user.groups.filter(name="store_keeper").exists()

# Create your views here.
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
@is_not_superuser
def list_items(request):
    global store_name
    #Check if user is in Store_keeper group
    storeKeeperMember = isStoreKeeper(request.user)
    if isStoreKeeper(request.user):
        Stock = yassa_stock
        store_name = "Yassa"
    else :
        Stock = internal_stock
        store_name = "Internal Stock"
    header = 'List of Items'
    tests = []
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all().order_by('-last_updated')
    for instance in queryset:
        reorder = instance.reorder_level
        reorder_min_critical = reorder*0.2
        tests.append([instance, int(reorder_min_critical)])
    
    context = {
        "header" : header,
        "title" : store_name,
        "queryset" : queryset,
        "form" : form,
        "instance_and_maxReorder" : tests,
        "store_name" : store_name,
        "storeKeeperMember" : storeKeeperMember,
    }
    #To create an automatic search on the model stock, instead of using AJAX
    if request.method == 'POST':
        #tests is a list that keeps data of the reorder level of each good in the stock
        tests = []
        queryset = Stock.objects.filter(
            item_name__icontains=form['item_name'].value(),
        ).order_by('-last_updated')
        
        for instance in queryset:
            print(instance)
            reorder = instance.reorder_level
            reorder_min_critical = reorder*0.2
            tests.append([instance, int(reorder_min_critical)])

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of item in internal stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['ITEM NAME', 'QUANTITY', 'REORDER LEVEL', 'ISSUE BY', 'LAST UPDATE'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.item_name, stock.quantity, stock.reorder_level, stock.issue_by, stock.last_updated])
            return response
        
        context = {
            "form" : form,
            "header" : header,
            "instance_and_maxReorder" : tests,
        }
    if isStoreKeeper(request.user):
        return render(request, "store/list_items.html", context)
    return render(request, "internal_stock/list_items.html", context)

@login_required
@is_not_superuser
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
@is_not_superuser
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    yassa_queryset = yassa_stock.objects.all()
    #check if the element exists in yassa stock
    if yassa_queryset.filter(item_name=queryset.item_name).exists():
        yassa_stock_item = yassa_stock.objects.get(item_name=queryset.item_name)
    else:
        yassa_stock_item = None
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            #change the item name in yassa stock
            if yassa_stock_item:
                instance = form.save(commit=False)
                yassa_stock_item.item_name = instance.item_name
                yassa_stock_item.save()
                instance.save()
            form.save()
            messages.success(request, "Successfully Updated")
            return redirect('/list_items')
        
    context = {
        'form' : form
    }
    return render(request, 'internal_stock/add_items.html', context)

@login_required
@is_not_superuser
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/')
    return render(request, 'internal_stock/delete_items.html')

@login_required
@is_not_superuser
def stock_detail(request, pk):
    global store_name
    queryset = Stock.objects.get(id=pk)
    context = {
        "queryset" : queryset,
        "store_name" : store_name
    }
    return render(request, "internal_stock/stock_detail.html", context)

@login_required
@is_not_superuser
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
@is_not_superuser
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
        instance.issue_to = "yassa"
        queryset = Stock.objects.get(id=pk)
        #To add to yassa stock
        if queryset.issue_to == 'yassa':
            internal_stock_item_name = queryset.item_name
            #Create item if not existing in the database of internal stock
            try:
                queryset_yassa = yassa_stock.objects.get(item_name=internal_stock_item_name)
            except yassa_stock.DoesNotExist:
                yassa_stock.objects.create(item_name=internal_stock_item_name, issue_by="Internal Stock")
                queryset_yassa = yassa_stock.objects.get(item_name=internal_stock_item_name)
            queryset_yassa.quantity += add_to_other_stock
            queryset_yassa.issue_by = "Internal Stock"
            queryset_yassa.receive_quantity = add_to_other_stock
            queryset_yassa.observations = instance.observations
            #Pull the trigger for the receiving stock
            queryset_yassa.issue_quantity = 0
            queryset_yassa.save()
        instance.save()
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
@is_not_superuser
def receive_items(request, pk):
    global store_name
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        print(type(instance.quantity))
        print(type(instance.receive_quantity))
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
@is_not_superuser
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
        if form['item_name'].value():
            queryset = StockHistory.objects.filter(
                item_name__icontains=form['item_name'].value(),
            ).order_by('-last_updated')
        
        if form['start_date'].value() and form['end_date'].value() :
            queryset = StockHistory.objects.filter(
                last_updated__range = [
                form['start_date'].value(),
                form['end_date'].value()
                ]
            ).order_by('-last_updated')
        #To save csv file
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="Internal Stock History.csv"'
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
    
@login_required
@is_not_superuser
#PDF generation
def getpdf(request, pk):
    queryset = Receipt.objects.get(id=pk)
    client_id = queryset.client_id
    if queryset.internal_stock_id:
        item_id = queryset.internal_stock_id
        item = Stock.objects.get(id=item_id)
    else:
        item_id = queryset.yassa_stock_id
        item = yassa_stock.objects.get(id=item_id)
    client = Client.objects.get(id=client_id)
    date = str(queryset.date)    
    filename = "receipt_"+str(client.id)+ str(client.first_name) + str(client.name) + date[:11]+".pdf"
    """data = [
        ['ID', 'First Name', 'Name','Item', 'Quantity','Price HT', 'Price TVA', 'Price TTC'],
        [client.id, client.first_name,client.name,item.item_name,queryset.quantity,queryset.total_ht,queryset.total_tva,queryset.total_ttc ]
    ]
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+filename+''
    """pdf = SimpleDocTemplate(filename,pagesize=letter)
    table = Table(data)
    #styling the table
    style = TableStyle(
        [
            ('BACKGROUND', (0,0), (7,0),colors.green),
            ('TEXTCOLOR', (0,0),(-1,0),colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1),'CENTER'),
            ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
            ('FONTSIZE',(0,0),(-1,0),14),
            ('BOTTOMPADDING',(0,0),(-1,0),12),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
            ('BOX', (0,0),(-1,-1),2,colors.black),
            ('GRID',(0,1),(-1,-1),2,colors.black),
        ]
    )
    table.setStyle(style)
    elements = []
    elements.append(table)
    pdf.build(elements)
    """
    p = canvas.Canvas(response,pagesize=letter)
    p.setFont("Times-Roman",20)
    p.drawString(20,700, "Receipt, client tax registration : " + str(client.tax_registration_number))
    p.setFont("Times-Roman",15)
    p.drawString(300,750, "Date : " +str(date[:11]))
    p.drawString(10,650, "ID :")
    p.drawString(110,650, str(client.id))
    p.drawString(10,600, "First Name :")
    p.drawString(110,600, str(client.first_name))
    p.drawString(10,550, "Name :")
    p.drawString(110,550, str(client.name))
    p.drawString(10,500, "Item Name :")
    p.drawString(110,500, str(item.item_name))
    p.drawString(10,450, "Quantity :")
    p.drawString(110,450, str(queryset.quantity))
    p.drawString(10,400, "TOTAL HT :")
    p.drawString(110,400, str(queryset.total_ht))
    p.drawString(10,350, "TOTAL TVA :")
    p.drawString(110,350, str(queryset.total_tva))
    p.drawString(10,300, "TOTAL TTC :")
    p.drawString(110,300, str(queryset.total_ttc))
    p.showPage()
    p.save()
    return response

@login_required
@is_not_superuser
def getpdf_invoice(request, pk):
    queryset = Invoice.objects.get(id=pk)
    provider_id = queryset.provider_id
    if queryset.internal_stock_id:
        item_id = queryset.internal_stock_id
        item = Stock.objects.get(id=item_id)
    else:
        item_id = queryset.yassa_stock_id
        item = yassa_stock.objects.get(id=item_id)
    provider = Provider.objects.get(id=provider_id)
    date = str(queryset.date)    
    filename = "invoice"+str(provider.id)+ str(provider.first_name) + str(provider.name) + date[:11]+".pdf"
    """data = [
        ['ID', 'First Name', 'Name','Item', 'Quantity','Price HT', 'Price TVA', 'Price TTC'],
        [provider.id, provider.first_name,provider.name,item.item_name,queryset.quantity,queryset.total_ht,queryset.total_tva,queryset.total_ttc ]
    ]
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+filename+''
    """pdf = SimpleDocTemplate(filename,pagesize=letter)
    table = Table(data)
    #styling the table
    style = TableStyle(
        [
            ('BACKGROUND', (0,0), (7,0),colors.green),
            ('TEXTCOLOR', (0,0),(-1,0),colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1),'CENTER'),
            ('FONTNAME',(0,0),(-1,0),'Courier-Bold'),
            ('FONTSIZE',(0,0),(-1,0),14),
            ('BOTTOMPADDING',(0,0),(-1,0),12),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
            ('BOX', (0,0),(-1,-1),2,colors.black),
            ('GRID',(0,1),(-1,-1),2,colors.black),
        ]
    )
    table.setStyle(style)
    elements = []
    elements.append(table)
    pdf.build(elements)
    """
    p = canvas.Canvas(response,pagesize=letter)
    p.setFont("Times-Roman",20)
    p.drawString(20,700, "Invoice, provider tax registration number : " + str(provider.tax_registration_number))
    p.setFont("Times-Roman",15)
    p.drawString(300,750, "Date : " +str(date[:11]))
    p.drawString(10,650, "ID :")
    p.drawString(110,650, str(provider.id))
    p.drawString(10,600, "First Name :")
    p.drawString(110,600, str(provider.first_name))
    p.drawString(10,550, "Name :")
    p.drawString(110,550, str(provider.name))
    p.drawString(10,500, "Item Name :")
    p.drawString(110,500, str(item.item_name))
    p.drawString(10,450, "Quantity :")
    p.drawString(110,450, str(queryset.quantity))
    p.drawString(10,400, "TOTAL HT :")
    p.drawString(110,400, str(queryset.total_ht))
    p.drawString(10,350, "TOTAL TVA :")
    p.drawString(110,350, str(queryset.total_tva))
    p.drawString(10,300, "TOTAL TTC :")
    p.drawString(110,300, str(queryset.total_ttc))
    p.showPage()
    p.save()
    return response