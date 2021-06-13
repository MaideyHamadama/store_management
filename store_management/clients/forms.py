from django import forms
from .models import Client, Receipt

class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'name', 'tax_registration_number', 'society', 'telephone', 'fax', 'mobile', 'email', 'adresse']
    
    #Validating the form
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('This field is required')
        return first_name
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required')
        return name
    
    def clean_tax_registration_number(self):
        tax_registration_number = self.cleaned_data.get('tax_registration_number')
        if not tax_registration_number:
            raise forms.ValidationError('This field is required')
        return tax_registration_number
    
    def clean_society(self):
        society = self.cleaned_data.get('society')
        if not society:
            raise forms.ValidationError('This field is required')
        return society
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile:
            raise forms.ValidationError('This field is required')
        return mobile
    
    def clean_adresse(self):
        adresse = self.cleaned_data.get('adresse')
        if not adresse:
            raise forms.ValidationError('This field is required')
        return adresse
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('This field is required')
        return email

class ClientSearchForm(forms.ModelForm):
    #We can add a field in a form individually not only from the model.py
    mobile = forms.CharField(required=False)
    email = forms.CharField(required=False)
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Client
        fields = []
        
class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'name', 'tax_registration_number', 'society', 'telephone', 'fax', 'mobile', 'email', 'adresse']

    #Validating the form
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('This field is required')
        return first_name
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('This field is required')
        return name
    
    def clean_tax_registration_number(self):
        tax_registration_number = self.cleaned_data.get('tax_registration_number')
        if not tax_registration_number:
            raise forms.ValidationError('This field is required')
        return tax_registration_number
    
    def clean_society(self):
        society = self.cleaned_data.get('society')
        if not society:
            raise forms.ValidationError('This field is required')
        return society
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not mobile:
            raise forms.ValidationError('This field is required')
        return mobile
    
    def clean_adresse(self):
        adresse = self.cleaned_data.get('adresse')
        if not adresse:
            raise forms.ValidationError('This field is required')
        return adresse
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('This field is required')
        return email

class ReceiptSearchForm(forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    class Meta:
        model = Receipt
        fields = ['client']

class ReceiptCreateForm(forms.ModelForm):
    #Validation of the form
    #To handle a double field validation internal_stock and yassa_stock
    def clean(self):
        cleaned_data = super().clean()
        internal_stock = cleaned_data.get('internal_stock')
        yassa_stock = cleaned_data.get('yassa_stock')
        if not yassa_stock and not internal_stock:
            raise forms.ValidationError('Either yassa stock or internal stock must be choosen')
        if yassa_stock and internal_stock:
            raise forms.ValidationError('Either yassa stock or internal stock must be choosen')

    def clean_total_ht(self):
        total_ht = self.cleaned_data.get('total_ht')
        if not total_ht:
            raise forms.ValidationError('This field is required')
        return total_ht
    
    def clean_total_tva(self):
        total_tva = self.cleaned_data.get('total_tva')
        if not total_tva:
            raise forms.ValidationError('This field is required')
        return total_tva
    
    def clean_total_ttc(self):
        total_ttc = self.cleaned_data.get('total_ttc')
        total_tva = self.cleaned_data.get('total_tva')
        total_ht = self.cleaned_data.get('total_ht')
        
        if not total_ttc:
            raise forms.ValidationError('This field is required')
        
        if total_ttc and total_tva and total_ht:
            if total_ttc < (total_ht + total_tva):
                raise forms.ValidationError('Error in the calculations')
        return total_ttc
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if not quantity:
            raise forms.ValidationError('This field is required')
        
        return quantity

    class Meta:
        model = Receipt
        fields = ['client','internal_stock','yassa_stock','quantity','total_ht', 'total_tva', 'total_ttc']