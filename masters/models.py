from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
import os

#### Company
class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    # You can add more fields if needed, like address, phone, etc.

    def __str__(self):
        return self.name


#  Status Colors
class StatusColor(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_code = models.CharField(max_length=50, unique=True)
    status_name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=7)  # e.g., "#FF0000"

    def __str__(self):
        return f"{self.status_name} ({self.color_code})"
    
# Sales Division
class SalesDivision(models.Model):
    div_id = models.AutoField(primary_key=True)
    div_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.div_name

#  Warehouse
class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.warehouse_name

#  Item Category
class ItemCategory(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100, unique=True)
    sales_division = models.ForeignKey(SalesDivision, on_delete=models.PROTECT, null=True)
    warehouses = models.ManyToManyField(Warehouse, related_name='item_categories')

    def __str__(self):
        warehouse_names = ", ".join(w.warehouse_name for w in self.warehouses.all())
        return f"{self.item_name} — {self.sales_division.div_name} — [{warehouse_names}]"
        
# utils.py or a models proxy section
from collections import namedtuple
ItemWarehouse = namedtuple('ItemWarehouse', ['item_id', 'warehouse_id', 'label'])


#  Vehicle Types
class VehicleType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_code = models.CharField(max_length=20, unique=True)
    type_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.type_name

####################################

def shipment_upload_path(instance, filename):
    """
    Store file in: shipments/assessments/shipment_<id>/<original_filename>
    """
    return os.path.join(
        "shipments",
        "assessments",
        f"shipment_{instance.id}",
        filename
    )


#  Shipment
class Shipment(models.Model):
    id = models.AutoField(primary_key=True)
    purchase_order_no = models.CharField(max_length=100)
    packing_list_ref = models.CharField(max_length=100)
    supplier_invoice = models.CharField(max_length=100,null=True, blank=True)
    order_date = models.DateField()
    expected_arrival_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=100,null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
    # masters/models.py (Shipment)
    c_date = models.DateField(null=True, blank=True)
    #remarks = models.TextField(blank=True, null=True)
    #vehicle_number = models.CharField(max_length=50, blank=True, null=True)
    #vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    #actual_arrival_date = models.DateField(blank=True, null=True)

    # NEW FIELDS
    #bank_doc_type = models.CharField(max_length=100, null=True, blank=True)

    BANK_DOC_TYPES = [
        ("DA", "DA"),
        ("DP", "DP"),
        ("LC", "LC"),
        ("TT", "TT"),
    ]

    bank_doc_type = models.CharField(
        max_length=10,
        choices=BANK_DOC_TYPES,
        null=True,
        blank=True
    )
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    send_to_clearing_agent = models.BooleanField(default=False)
    send_date = models.DateField(null=True, blank=True)

    # Clearing agent part
    assessment_document = models.FileField(
        upload_to=shipment_upload_path,
        null=True,
        blank=True
    )
    assessment_uploaded_date = models.DateField(null=True, blank=True)

    # Bank manager stage
    payment_marked = models.BooleanField(default=False)
    payment_marked_date = models.DateField(null=True, blank=True)

    # MD final approval
    duty_paid = models.BooleanField(default=False)
    duty_paid_date = models.DateField(null=True, blank=True)

    class Meta:
        permissions = [
            ("can_create_shipment", "Can create shipment"),
            ("can_update_arrival_status", "Can update shipment arrival status"),
            ("can_start_unloading", "Can mark unloading started"),
            ("can_complete_unloading", "Can mark unloading complete"),
            ("can_view_admin_dashboard", "Can view admin dashboard"),
            ("can_view_warehouse_dashboard", "Can view warehouse dashboard"),

             # NEW permissions for workflow
            ("can_update_bank_docs", "Can update bank documents"),
            ("can_upload_assessment", "Can upload assessment document"),
            ("can_mark_payment", "Bank Manager can mark payment done"),
            ("can_approve_duty_paid", "MD can approve duty paid"),
        ]

    def __str__(self):
        return f"PO: {self.purchase_order_no}"

    def get_status(self):
        """
        Dynamically computes overall shipment status based on its ShipmentDetails.
        """
        detail_statuses = self.details.values_list('status__status_name', flat=True)

        if not detail_statuses:
            return "No details"

        if all(status == "Unloading completed" for status in detail_statuses):
            return "Completed"
        elif any(status == "Currently being unloaded" for status in detail_statuses):
            return "Unloading in progress"
        elif all(status == "Shipment created, not yet arrived" for status in detail_statuses):
            return "Pending"
        elif any(status == "Delayed" for status in detail_statuses):
            return "Delayed"
        else:
            return "Partially processed"
        
        # Now extend with bank/clearing flow
        if self.send_to_clearing_agent and not self.assessment_document:
            return f"{shipment_status} - Sent to Clearing Agent"
        if self.assessment_document and not self.duty_paid:
            return f"{shipment_status} - Awaiting Duty Payment"
        if self.duty_paid:
            return f"{shipment_status} - Duty Paid"

# Shipment Detail (line items / consignments)
class ShipmentDetail(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='details')
    item_category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT)
    sales_division = models.ForeignKey(SalesDivision, on_delete=models.PROTECT, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, null=True, blank=True)
    status = models.ForeignKey(StatusColor, on_delete=models.PROTECT, null=True, blank=True)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_number = models.CharField(max_length=50, blank=True, null=True)
    actual_arrival_date = models.DateField(blank=True, null=True)
    unloading_start_time = models.DateTimeField(blank=True, null=True)
    unloading_end_time = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    is_delayed = models.BooleanField(default=False)
    delay_reason = models.TextField(blank=True, null=True)
    demurrage_start_date = models.DateField(blank=True, null=True)
    demurrage_end_date = models.DateField(blank=True, null=True)
    demurrage_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.shipment.purchase_order_no} | {self.item_category} | {self.sales_division} | {self.warehouse}"

    def unloading_duration(self):
        if self.unloading_start_time and self.unloading_end_time:
            return self.unloading_end_time - self.unloading_start_time
        return None

    def days_delayed(self):
        if self.actual_arrival_date:
            delay_days = (self.actual_arrival_date - self.shipment.expected_arrival_date).days
            return delay_days if delay_days > 0 else 0
        return 0

    def is_under_demurrage(self):
        today = timezone.now().date()
        return self.demurrage_start_date and self.demurrage_end_date and self.demurrage_start_date <= today <= self.demurrage_end_date

#  Shipment Status History (audit trail)
class ShipmentStatusHistory(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusColor, on_delete=models.PROTECT)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)


#from .models import Warehouse
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # = models.ManyToManyField('Warehouse', blank=True)
    #warehouses = models.ManyToManyField(Warehouse, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} Profile"



