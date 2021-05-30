from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages#Use for notifcation instead of using javascript
from django.contrib.auth.decorators import login_required
from .models import Provider, Invoice
from internal_stock.models import Stock as internal_stock
from store.models import Stock as yassa_stock
from clients.models import Client
from .forms import *
import csv
from internal_stock.decorators import is_not_superuser
# Create your views here.

@login_required
@is_not_superuser
def home(request):
    header = "List of Providers"
    #Request for providers from the providers table
    queryset = Provider.objects.all()
    #Search form of provider
    form = ProviderSearchForm(request.POST or None)
    context = {
        "queryset" : queryset,
        "header" : header,
        "form" : form,
    }
    
    #If the user submit the provider search form
    if request.method == 'POST' :       
        if form['mobile'].value():
            queryset = Provider.objects.filter(mobile__icontains=form['mobile'].value())
            
        if form['email'].value():
            queryset = Provider.objects.filter(email__icontains=form['email'].value())
    
        if form['export_to_CSV'].value() == True:
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="List of Providers.csv"'
                writer = csv.writer(response)
                writer.writerow(['FIRST NAME', 'NAME', 'TAX REGISTRATION NUMBER', 'SOCIETY', 'TELEPHONE', 'FAX', 'MOBILE', 'EMAIL', 'ADRESSE'])
                instance = queryset
                for provider in instance:
                    writer.writerow([provider.first_name, provider.name, provider.tax_registration_number, provider.society, provider.telephone, provider.fax, provider.mobile, provider.email, provider.adresse])
                return response
        
        context = {
        "queryset" : queryset,
        "header" : header,
        "form" : form,
        }
    
    return render(request, "providers/list_provider.html", context)

@login_required
@is_not_superuser
def add_provider(request):
    header = "Add Provider"
    #Add form of provider
    form = ProviderCreateForm(request.POST or None)
    #Form validation
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully Saved")
        return redirect('/providers')
    context = {
        "header" : header,
        "form" : form,
    }
    return render(request, "providers/add_provider.html", context)
    
@login_required
@is_not_superuser
def update_provider(request, pk):
    queryset = Provider.objects.get(id=pk)
    header = "Update provider " + queryset.first_name + " " + queryset.name
    form = ProviderUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = ProviderUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated")
            return redirect('/providers')
        
    context = {
        'header' : header,
        'form' : form
    }
    return render(request, 'providers/add_provider.html', context)

@login_required
@is_not_superuser
def delete_provider(request, pk):
    queryset = Provider.objects.get(id=pk)
    context = {
        "queryset" : queryset,
    }
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/')
    return render(request, 'providers/delete_provider.html', context)

@login_required
@is_not_superuser
def sell_invoice(request):
    header = "List of all invoices"
    queryset = Invoice.objects.all().order_by('-date')
    form = InvoiceSearchForm(request.POST or None)
    context = {
        'queryset' : queryset,
        'header' : header,
        'form' : form
    }
    
    if request.method == 'POST' :
        if form['provider'].value():
            queryset = Invoice.objects.filter(provider_id = form['provider'].value()).order_by('-date')
            provider_info = Provider.objects.get(id=form['provider'].value())
            provider_trn = provider_info.tax_registration_number

        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of Invoice.csv"'
            writer = csv.writer(response)
            writer.writerow(['ID', 'DATE'])
            instance = queryset
            for invoice in instance:
                writer.writerow([invoice.id, invoice.date])
            return response
    
        context = {
        "queryset" : queryset,
        "provider_trn" : provider_trn,
        "header" : header,
        "form" : form,
        }
    
    return render(request,'providers/invoice.html', context)


@login_required
@is_not_superuser
def add_invoice(request):
    header = "Add Invoice"
    #Add form of client
    form = InvoiceCreateForm(request.POST or None)
    #Form validation
    if form.is_valid():
        instance = form.save(commit=False)
        #INTERNAL STOCK TRANSACTION
        if instance.internal_stock:
            internal_stock_item_name = instance.internal_stock
            internal_stock_item = internal_stock.objects.get(item_name=internal_stock_item_name)
            if internal_stock_item.id:
                queryset = internal_stock.objects.get(id=internal_stock_item.id)
                queryset.quantity += instance.quantity
                queryset.receive_quantity = instance.quantity
                #Get client name
                provider = instance.provider
                queryset_provider = Provider.objects.get(id=provider.id)
                queryset.issue_by = str(queryset_provider.first_name)
                queryset.issue_quantity = 0
                queryset.receive_by = "Internal"
                queryset.observations = None
                queryset.back_to_usine = None
                queryset.material_status = None
                queryset.save()
            messages.success(request, "Successfully Saved")
            instance.save()
            return redirect('/invoice')
        else:
            yassa_stock_item_name = instance.yassa_stock
            yassa_stock_item = yassa_stock.objects.get(item_name=yassa_stock_item_name)
            if yassa_stock_item.id:
                yassa_stock_quantity = instance.quantity
                queryset = yassa_stock.objects.get(id=yassa_stock_item.id)
                queryset.issue_quantity = 0
                queryset.quantity += yassa_stock_quantity
                queryset.receive_quantity = yassa_stock_quantity
                #Get client name
                provider = instance.provider
                queryset_provider = Provider.objects.get(id=provider.id)
                queryset.issue_by = str(queryset_provider.first_name)
                queryset.receive_by = "Internal"
                queryset.observations = None
                queryset.back_to_usine = None
                queryset.material_status = None                
                queryset.save()
            messages.success(request, "Successfully Saved")
            instance.save()
            return redirect('/invoice')
    context = {
        "header" : header,
        "form" : form,
    }
    return render(request, "providers/add_invoice.html", context)

def delete_invoice(request, pk):
    queryset = Invoice.objects.get(id=pk)
    context = {
        "queryset" : queryset,
    }
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'Successfully deleted')
        return redirect('/')
    return render(request, 'providers/delete_provider.html', context)