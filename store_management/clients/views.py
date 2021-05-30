from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages#Use for notifcation instead of using javascript
from django.contrib.auth.decorators import login_required
from .models import Client as clients
from .models import Receipt
from internal_stock.models import Stock as internal_stock
from store.models import Stock as yassa_stock
from .forms import *
import csv
from internal_stock.decorators import is_not_superuser
from django.utils.translation import get_language
# Create your views here.

@login_required
@is_not_superuser
def home(request):
    header = "LIST OF CLIENTS"
    #Request for clients from the clients table
    queryset = Client.objects.all()
    #Search form of client
    form = ClientSearchForm(request.POST or None)
    context = {
        "queryset" : queryset,
        "header" : header,
        "form" : form,
    }
    
    #If the user submit the client search form
    if request.method == 'POST' :
        if form['mobile'].value():
            queryset = Client.objects.filter(mobile__icontains=form['mobile'].value())
            
        if form['email'].value():
            queryset = Client.objects.filter(email__icontains=form['email'].value())
    
        if form['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="List of Clients.csv"'
                writer = csv.writer(response)
                writer.writerow(['FIRST NAME', 'NAME', 'TAX REGISTRATION NUMBER', 'SOCIETY', 'TELEPHONE', 'FAX' , 'MOBILE', 'EMAIL', 'ADRESSE'])
                instance = queryset
                for client in instance:
                    writer.writerow([client.first_name, client.name, client.tax_registration_number,client.society,client.telephone,client.fax,client.mobile,client.email,client.adresse])
                return response
        
        context = {
        "queryset" : queryset,
        "header" : header,
        "form" : form,
        }
    
    return render(request, "clients/list_clients.html", context)

@login_required
@is_not_superuser
def add_client(request):
    header = "Add Client"
    #Add form of client
    form = ClientCreateForm(request.POST or None)
    #Form validation
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully Saved")
        return redirect('/clients')
    context = {
        "header" : header,
        "form" : form,
    }
    return render(request, "clients/add_client.html", context)
    
@login_required
@is_not_superuser
def update_client(request, pk):
    queryset = Client.objects.get(id=pk)
    header = "Update client " + queryset.first_name + " " + queryset.name
    form = ClientUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = ClientUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return redirect('/clients')
        
    context = {
        'header' : header,
        'form' : form
    }
    return render(request, 'clients/add_client.html', context)

@login_required
@is_not_superuser
def delete_client(request, pk):
    current_language = get_language()
    queryset = Client.objects.get(id=pk)
    context = {
        "queryset" : queryset,
    }
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/')
    return render(request, 'clients/delete_client.html', context)

@login_required
@is_not_superuser
def receipt(request):
    header = "List of all receipts"
    queryset = Receipt.objects.all().order_by('-date')
    form = ReceiptSearchForm(request.POST or None)
    context = {
        'queryset' : queryset,
        'header' : header,
        'form' : form
    }
    
    if request.method == 'POST' :
        queryset = Receipt.objects.filter(
            client_id=form['client'].value(),
        ).order_by('-date')
        
        client_search_queryset = clients.objects.get(id=form['client'].value())
        client_trn = client_search_queryset.tax_registration_number
        print(client_trn)
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of Receipt.csv"'
            writer = csv.writer(response)
            writer.writerow(['CLIENT ID', 'DATE'])
            instance = queryset
            for receipt in instance:
                writer.writerow([receipt.client_id, receipt.date])
            return response
    
        context = {
        "queryset" : queryset,
        "client_trn" : client_trn,
        "header" : header,
        "form" : form,
        }
    
    return render(request,'clients/receipt.html', context)

@login_required
@is_not_superuser
def add_receipt(request):
    header = "Add Receipt"
    #Add form of client
    form = ReceiptCreateForm(request.POST or None)
    #Form validation
    if form.is_valid():
        instance = form.save(commit=False)
        #INTERNAL STOCK TRANSACTION
        if instance.internal_stock:
            internal_stock_item_name = instance.internal_stock
            internal_stock_item = internal_stock.objects.get(item_name=internal_stock_item_name)
            if internal_stock_item.id:
                internal_stock_quantity = instance.quantity
                queryset = internal_stock.objects.get(id=internal_stock_item.id)
                if internal_stock_quantity > queryset.quantity :
                    messages.warning(request, "The issue quantity " + str(internal_stock_quantity) + " is above the stock quantity.")
                    return redirect('/stock_detail/' + str(queryset.id))
                queryset.receive_quantity = 0
                queryset.quantity -= internal_stock_quantity
                queryset.issue_quantity = internal_stock_quantity
                #Get client name
                client = instance.client
                queryset_client = Client.objects.get(id=client.id)
                queryset.issue_to = str(queryset_client.first_name)
                queryset.issue_by = "Internal"
                queryset.observations = None
                queryset.back_to_usine = None
                queryset.material_status = None                
                queryset.save()
            messages.success(request, "Successfully Saved")
            #print(instance.client)
            instance.save()
            return redirect('/receipt')
        else:
            yassa_stock_item_name = instance.yassa_stock
            yassa_stock_item = yassa_stock.objects.get(item_name=yassa_stock_item_name)
            if yassa_stock_item.id:
                yassa_stock_quantity = instance.quantity
                queryset = yassa_stock.objects.get(id=yassa_stock_item.id)
                if yassa_stock_quantity > queryset.quantity :
                    messages.warning(request, "The issue quantity " + str(yassa_stock_quantity) + " is above the stock quantity.")
                    return redirect('/stock_detail/' + str(queryset.id))
                queryset.receive_quantity = 0
                queryset.quantity -= yassa_stock_quantity
                queryset.issue_quantity = yassa_stock_quantity
                #Get client name
                client = instance.client
                queryset_client = Client.objects.get(id=client.id)
                queryset.issue_to = str(queryset_client.first_name)
                queryset.issue_by = "Internal"
                queryset.observations = None
                queryset.back_to_usine = None
                queryset.material_status = None                
                queryset.save()
            messages.success(request, "Successfully Saved")
            instance.save()
            return redirect('/receipt')
    context = {
        "header" : header,
        "form" : form,
    }
    return render(request, "clients/add_receipt.html", context)


@login_required
@is_not_superuser
def delete_receipt(request, pk):
    current_language = get_language()
    queryset = Receipt.objects.get(id=pk)
    context = {
        "queryset" : queryset,
    }
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/')
    return render(request, 'clients/receipt.html', context)