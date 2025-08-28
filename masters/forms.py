from django import forms
from .models import (
    ItemCategory, VehicleType, StatusColor, SalesDivision,
    Shipment, ShipmentDetail, Warehouse
)

# Ã°Å¸â€œÂ¦ Item Category Form
class ItemCategoryForm(forms.ModelForm):
    sales_division = forms.ModelChoiceField(
        queryset=SalesDivision.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        empty_label="Please select",
        required=False
    )

    class Meta:
        model = ItemCategory
        fields = ['item_name', 'sales_division', 'warehouses']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'warehouses': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }


#  vehicle types
class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehicleType
        fields = ['type_code', 'type_name', 'is_active']

## Status
from django import forms
from .models import StatusColor

class StatusColorForm(forms.ModelForm):
    class Meta:
        model = StatusColor
        fields = ['status_code','status_name', 'color_code']
        widgets = {
            'status_code': forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),

            'status_name': forms.TextInput(attrs={'class': 'form-control'}),
            'color_code': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
        }



################# sales division



class SalesDivisionForm(forms.ModelForm):
    class Meta:
        model = SalesDivision
        fields = ['div_name']
        widgets = {
            'div_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


###################### Shipments


# ðŸ“¦ Shipment Form (parent)
class ShipmentForm(forms.ModelForm):
    item_categories = forms.ModelMultipleChoiceField(
        queryset=ItemCategory.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select select2'}),
        required=False,
        label="Select Items"
    )
    class Meta:
        model = Shipment
        exclude = ['created_by', 'created_at']
        widgets = {
            'purchase_order_no': forms.TextInput(attrs={'class': 'form-control'}),
            'packing_list_ref': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_invoice': forms.TextInput(attrs={'class': 'form-control'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expected_arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'c_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-select select2'}),
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 
            'bank_doc_type': forms.Select(attrs={'class': 'form-select select2'}),  # dropdown
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


#################################
class BankDocForm(forms.ModelForm):
    """Bank controller can update bank docs & send to clearing"""
    class Meta:
        model = Shipment
        fields = [
            "bank_doc_type",
            "reference_number",
            "send_to_clearing_agent",
            "send_date",
        ]


class AssessmentForm(forms.ModelForm):
    """Clearing agent can upload assessment doc"""
    class Meta:
        model = Shipment
        fields = ["assessment_document"]


class MarkPaymentForm(forms.ModelForm):
    """Bank manager marks payment"""
    class Meta:
        model = Shipment
        fields = ["payment_marked", "payment_marked_date"]


class DutyApprovalForm(forms.ModelForm):
    """MD approves duty paid"""
    class Meta:
        model = Shipment
        fields = ["duty_paid", "duty_paid_date"]


# forms.py
class BankControllerForm(forms.ModelForm):
    """Bank Controller updates send_to_clearing_agent and send_date"""
    class Meta:
        model = Shipment
        fields = ["send_to_clearing_agent", "send_date"]


# forms.py


class AssessmentUploadForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['assessment_document']





# ðŸ“¦ Shipment Detail Form
class ShipmentDetailForm(forms.ModelForm):


    class Meta:
        model = ShipmentDetail
        exclude = [
            'shipment',
            'vehicle_type',
            'vehicle_number',
            'actual_arrival_date',
            'unloading_start_time',
            'unloading_end_time',
            'remarks',
            'is_delayed',
            'delay_reason',
            'demurrage_start_date',
            'demurrage_end_date',
            'demurrage_amount',
        ]
        widgets = {
            'item_category': forms.Select(attrs={'class': 'form-select select2'}),
            'sales_division': forms.Select(attrs={'class': 'form-select select2'}),
            'warehouse': forms.Select(attrs={'class': 'form-select select2'}),
            'status': forms.Select(attrs={'class': 'form-select select2'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        


################shipment Arrivals







###################

#  Warehouse Form
# ðŸ“¦ Warehouse Form
class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['warehouse_name', 'is_active']
        widgets = {
            'warehouse_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



################

##################  Usres 

from django import forms
from django.contrib.auth.models import User, Group

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    #warehouses = forms.ModelMultipleChoiceField(queryset=Warehouse.objects.all(), required=False)
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'warehouse']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
            
            
################# shipment Arrival Update
from django import forms
from .models import ShipmentDetail, StatusColor
from django.utils import timezone

class ArrivalUpdateForm(forms.ModelForm):
    class Meta:
        model = ShipmentDetail
        fields = ['status', 'actual_arrival_date', 'vehicle_type', 'vehicle_number']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control select2'}),
            'actual_arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control select2'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre‐select the “Shipment arrived at warehouse” status by default
        arrived = StatusColor.objects.filter(
            status_name="Shipment arrived at warehouse"
        ).first()
        if arrived:
            self.fields['status'].initial = arrived
        # default actual_arrival_date to today
        self.fields['actual_arrival_date'].initial = timezone.now().date()

###############  
# forms.py
from django import forms
from .models import ItemCategory

class ItemWarehouseSelectionForm(forms.Form):
    item_warehouses = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=True,
        label="Select Item-Warehouse Combinations"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = []
        for item in ItemCategory.objects.prefetch_related('warehouses'):
            for wh in item.warehouses.all():
                key = f"{item.pk}_{wh.pk}"
                label = f"{item.item_name} — {wh.warehouse_name}"
                choices.append((key, label))

        self.fields['item_warehouses'].choices = choices



####################

from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']  # Include other fields if you add them later
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
        }
        labels = {
            'name': 'Company Name'
        }