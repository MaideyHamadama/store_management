from django import forms
from .models import Stock, StockHistory

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reference', 'item_name', 'quantity', 'reorder_level', 'issue_by']
    
    #Validating the form
    def clean_reference(self):
        reference = self.cleaned_data.get('reference')
        if not reference:
            raise forms.ValidationError('This field is required')
        return reference
    
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if not quantity:
            raise forms.ValidationError('This field is required')
        return quantity
    
    def clean_reorder_level(self):
        reorder_level = self.cleaned_data.get('reorder_level')
        if not reorder_level:
            raise forms.ValidationError('This field is required')
        return reorder_level
    
class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    class Meta:
        model = StockHistory
        fields = ['item_name', 'start_date', 'end_date']
        
class StockSearchForm(forms.ModelForm):
    #We can add a field in a form individually not only from the model.py
    export_to_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['item_name']
        
class StockUpdateForm(forms.ModelForm):   
    class Meta:
        model = Stock
        fields = ['item_name', 'reference']
        
    #Validating the form
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if item_name == None:
            raise forms.ValidationError('This field is required')
        return item_name

class IssueForm(forms.ModelForm):
    #Validating the form
    def clean_issue_quantity(self):
        issue_quantity = self.cleaned_data.get('issue_quantity')
        if not issue_quantity:
            raise forms.ValidationError('This field is required')
        
        if issue_quantity <= 0:
            raise forms.ValidationError('The quantity must be greater than 0')
        return issue_quantity
    
    def clean_issue_to(self):
        list_stores = ['internal']
        issue_to = self.cleaned_data.get('issue_to')
        if not issue_to :
            raise forms.ValidationError('This field is required')
        
        if issue_to.lower() not in list_stores:
            raise forms.ValidationError('This store is not known')
        return issue_to
    
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to', 'observations']
        
class ReceiveForm(forms.ModelForm):
    def clean_receive_quantity(self):
        receive_quantity = self.cleaned_data.get('receive_quantity')
        if not receive_quantity:
            raise forms.ValidationError('This field is required')
        return receive_quantity
    
    def clean_issue_by(self):
        issue_by = self.cleaned_data.get('issue_by')
        if not issue_by:
            raise forms.ValidationError('This field is required')
        return issue_by
    
    class Meta:
        model = Stock
        fields = ['receive_quantity', 'issue_by', 'back_to_usine', 'material_status', 'observations']
        
class ReorderLevelForm(forms.ModelForm):
    
    class Meta:
        model = Stock
        fields = ['reorder_level']
        
    def clean_reorder_level(self):
        reorder_level = self.cleaned_data.get('reorder_level')
        if not reorder_level:
            raise forms.ValidationError('This field is required')
        return reorder_level