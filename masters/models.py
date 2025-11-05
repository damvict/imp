from django.db import models,transaction
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from datetime import datetime
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Max

################ functions
def generate_shipment_code(shipment_type):
    """
    Generate a unique shipment_code and shipment_sequence safely.
    Format: <TYPE>-<YEAR>-<SEQUENCE>
    Example: IMP-2025-001
    """
    year = timezone.now().year
    prefix = shipment_type or "IMP"

    # Start a transaction to prevent race conditions

    with transaction.atomic():
        last_sequence = (
            Shipment.objects
            .select_for_update()
            .aggregate(max_seq=Max("shipment_sequence"))["max_seq"] or 0
        )
        new_sequence = last_sequence + 1
        shipment_code = f"{prefix}-{year}-{new_sequence:03d}"
        return shipment_code, new_sequence




################## end




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
    
class Supplier(models.Model):
    supplier_code = models.CharField(max_length=20, unique=True)
    supplier_name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.supplier_name
    
class ClearingAgent(models.Model):
    agent_code = models.CharField(max_length=20, unique=True)
    agent_name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.agent_name




class Bank(models.Model):
    b_id = models.AutoField(primary_key=True)
    b_name = models.CharField(max_length=255)
    accno = models.CharField(max_length=100)
    branch = models.CharField(max_length=255)

    od = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    lc = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    imp = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    da = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    notes = models.TextField(null=True, blank=True)
    edate = models.DateField(auto_now_add=True)  # Current date on insert
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.b_name} - {self.accno}"

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


def shipment_payref_upload_path(instance, filename):
    """
    Store file in: shipments/payref/shipment_<id>/<original_filename>
    """
    return os.path.join(
        "shipments",
        "payref",
        f"shipment_{instance.id}",
        filename
    )


#  Shipment
class Shipment(models.Model):

    ################# New Arrival Notice 
    id = models.AutoField(primary_key=True)  
    shipment_sequence = models.IntegerField(default=0)
    shipment_code = models.CharField(max_length=20, unique=True, blank=True, null=True)      
    bl = models.CharField(max_length=100,default=0)
    vessel = models.CharField(max_length=200,default=' ')
    supplier_invoice = models.CharField(max_length=100,null=True, blank=True)
    order_date = models.DateField()  ########### Notice  arival date
    expected_arrival_date = models.DateField()  ############ ETA
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=100,null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)  
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    cbm = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    ship_status=models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    container=models.CharField(max_length=200,default=' ')

    ############### 2nd stage Shiment 
    packing_list_ref = models.CharField(max_length=100)
    c_date = models.DateTimeField(null=True, blank=True)
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
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

   #################   clearing Agent
    send_to_clearing_agent = models.BooleanField(default=False)
    send_date = models.DateTimeField(null=True, blank=True)   
    clearing_agent = models.ForeignKey(ClearingAgent, on_delete=models.SET_NULL, null=True, blank=True)
    C_Process_Initiated= models.BooleanField(default=False)
    C_Process_Initiated_date = models.DateTimeField(null=True, blank=True)   
    C_Process_completed= models.BooleanField(default=False)
    C_Process_completed_date = models.DateTimeField(null=True, blank=True)  

    arrival_at_warehouse= models.BooleanField(default=False)
    arrival_at_warehouse_date= models.DateTimeField(null=True, blank=True) 

    departure_at_warehouse= models.BooleanField(default=False)
    departure_at_warehouse_date= models.DateTimeField(null=True, blank=True)  

    grn_upload_at_warehouse= models.BooleanField(default=False)
    grn_upload_at_warehouse_date= models.DateTimeField(null=True, blank=True)  

    grn_complete_at_warehouse= models.BooleanField(default=False)
    grn_complete_at_warehouse_date= models.DateTimeField(null=True, blank=True)  


    ############# CA send to us
    assessment_document = models.FileField(
        upload_to=shipment_upload_path,
        null=True,
        blank=True
    )
    assessment_uploaded_date = models.DateTimeField(null=True, blank=True)
    total_duty_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # NEW

    # Bank manager stage
    payment_marked = models.BooleanField(default=False)
    payment_marked_date = models.DateTimeField(null=True, blank=True)
    duty_paid_bank=models.CharField(max_length=200, null=True,blank=True)
    send_to_clearing_agent_payment = models.BooleanField(default=False)
    send_to_clearing_agent_payment_date = models.DateTimeField(null=True, blank=True)
    payref_document_ref = models.CharField(max_length=100,blank=True, null=True) 
    payref_document = models.FileField(
        upload_to=shipment_payref_upload_path,
        null=True,
        blank=True
    )
    PAYMENT_TYPES = [
        ("BT", "Bank Transfer"),
        ("LC", "Letter of Credit"),
        ("CP", "Cash Payment"),
    ]
    payment_type = models.CharField(max_length=2, choices=PAYMENT_TYPES, null=True, blank=True)
    pay_note = models.TextField(null=True, blank=True)

    # MD final approval
    duty_paid = models.BooleanField(default=False)
    duty_paid_date = models.DateTimeField(null=True, blank=True)

    # --- (NEW) ---
    SHIPMENT_TYPES = [
        ("IMP", "IMP"),
        ("EXP", "EXP"),
    ]
    shipment_type = models.CharField(max_length=10, choices=SHIPMENT_TYPES, default="IMP")

    INCOTERMS = [
        ("FOB", "Free On Board"),
        ("CIF", "Cost, Insurance, and Freight"),
        ("EXW", "Ex Works"),
        ("DDP", "Delivered Duty Paid"),
        ("DAP", "Delivered At Place"),
    ]
    incoterm = models.CharField(max_length=10, choices=INCOTERMS, null=True, blank=True)

    TRANSPORT_MODES = [
        ("SEA", "Sea"),
        ("AIR", "Air"),
        ("LAND", "Land"),
    ]
    transport_mode = models.CharField(max_length=10, choices=TRANSPORT_MODES, null=True, blank=True)

    origin_country = models.CharField(max_length=100, null=True, blank=True)
    destination_port = models.CharField(max_length=100, null=True, blank=True)

    


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
        return f"{self.shipment_code or 'Unassigned'}"
    

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
        
    def save(self, *args, **kwargs):
        if not self.shipment_code:
            code, seq = generate_shipment_code(self.shipment_type)
            self.shipment_code = code
            self.shipment_sequence = seq
        super().save(*args, **kwargs)

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
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, null=True, blank=True)

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



class BankDocument(models.Model):
    DOC_TYPES = [
        ("LC", "Letter of Credit"),
        ("DA", "Documents Against Acceptance"),
        ("DP", "Documents Against Payment"),
        ("TT", "Telegraphic Transfer"),
        ("IMP", "Import Loan"),
    ]

    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="bank_docs")
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, null=True, blank=True)

    doc_type = models.CharField(max_length=10, choices=DOC_TYPES)
    reference_number = models.CharField(max_length=100, blank=True, null=True)

   # amount = models.DecimalField(max_digits=15, decimal_places=2)
    amount = models.DecimalField(
    max_digits=15,
    decimal_places=2,
    null=True,
    blank=True   # allows the form to accept empty values
)
    issue_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)  # e.g. LC maturity, IMP loan repayment
    settled = models.BooleanField(default=False)
    settlement_date = models.DateField(null=True, blank=True)

    # For LC → Import Loan conversion
    converted_to_imp = models.BooleanField(default=False)
    imp_reference = models.CharField(max_length=100, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_type} for Shipment {self.shipment.id} - {self.reference_number}"



##################################################################################

@receiver(post_save, sender=Shipment)
def create_bank_document(sender, instance, created, **kwargs):
    if created and instance.bank_doc_type and instance.bank:
        # Use the amount entered in Shipment form
        amount = instance.amount or 0

        # Use c_date or order_date or today as issue_date
        issue_date = instance.c_date or instance.order_date or timezone.now().date()

        BankDocument.objects.create(
            shipment=instance,
            bank=instance.bank,
            doc_type=instance.bank_doc_type,
            reference_number=instance.reference_number or "",
            amount=amount,
            issue_date=issue_date,
            due_date=None,  # No due date calculation
            created_by=instance.created_by
        )


#######################################################################################
class ShipmentPhaseMaster(models.Model):
    phase_code = models.CharField(max_length=50, unique=True)  # e.g., ARRIVAL_NOTICE
    phase_name = models.CharField(max_length=100)              # e.g., Arrival Notice Received
    order = models.PositiveIntegerField(default=0)             # sequence of phase in journey
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.order} - {self.phase_name}"



class ShipmentPhase(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="phases")
    phase_code = models.CharField(max_length=50)  # e.g., ARRIVAL_NOTICE
    phase_name = models.CharField(max_length=100) # e.g., Arrival Notice Received
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)  # sequence in timeline


from django.utils import timezone

class ShipmentDispatch(models.Model):
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE, related_name="dispatch")
    truck_no = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100)
    driver_license = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=20)
    transport_company = models.CharField(max_length=150)
    estimated_delivery = models.DateTimeField()
    delivery_address = models.TextField()
    special_instructions = models.TextField(blank=True, null=True)

    truck_arrived = models.BooleanField(default=False)
    truck_arrived_date = models.DateTimeField(null=True, blank=True)
    truck_depature = models.BooleanField(default=False)
    truck_depature_date = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispatch for {self.shipment.shipment_code}"

    def save(self, *args, **kwargs):
        """Whenever dispatch is created or updated, mark shipment process completed."""
        is_new = self._state.adding  # True if creating new record
        super().save(*args, **kwargs)
        if is_new:
            self.shipment.C_Process_completed = True
            self.shipment.C_Process_completed_date = timezone.now()
            self.shipment.save(update_fields=["C_Process_completed", "C_Process_completed_date"])


###################################### Functions

