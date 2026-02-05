from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Shipment, ShipmentPhase, ShipmentPhaseMaster, BankDocument
from django.utils.dateparse import parse_date
from django.db import transaction


from datetime import date

def _to_date(value):
    """
    Accepts str | date | None and returns date | None
    """
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return parse_date(value)
    return None


def create_arrival_notice(data, user):
    company = data.get('company')
    supplier = data.get('supplier')

    shipment = Shipment.objects.create(
        bl=data.get('bl', '0'),
        vessel=data.get('vessel', ''),
        order_date=_to_date(data.get('order_date')),
        expected_arrival_date=_to_date(data.get('expected_arrival_date')),
        cbm=data.get('cbm'),
        remark=data.get('remark', ''),
        #company =data.get('company'),
        #supplier=data.get('supplier'),
        company_id=company.id if hasattr(company, 'id') else company,
        supplier_id=supplier.id if hasattr(supplier, 'id') else supplier,

        container=data.get('container', ''),
        ship_status=1,
        created_by=user,
    )

    phase_master = ShipmentPhaseMaster.objects.get(id=1)
    ShipmentPhase.objects.create(
        shipment=shipment,
        phase_code=phase_master.phase_code,
        phase_name=phase_master.phase_name,
        completed=True,
        completed_at=timezone.now(),
        updated_by=user,
        order=phase_master.order,
    )

    return shipment


def update_shipment_stage(data, user):
    currency = data.get('currency')
    bank = data.get('bank')

    with transaction.atomic():
        shipment = get_object_or_404(Shipment, id=data.get('shipment_id'))
        shipment.bank_doc_type = data.get('bank_doc_type')
        shipment.reference_number = data.get('reference_number')
        #shipment.bank = data.get('bank')
        shipment.bank_id = bank if bank else None
        ##shipment.currency = data.get('currency')
        shipment.currency_id = currency if currency else None
        shipment.amount = data.get('amount')           # foreign amount
        shipment.amount_lkr = data.get('amount_lkr') 
        shipment.c_date = _to_date(data.get('due_date'))
        ##shipment.expected_arrival_date = (
        ##_to_date(data.get('expected_arrival_date'))
       ## or shipment.expected_arrival_date
    ##)
        shipment.shipment_type = data.get('shipment_type')
        shipment.incoterm = data.get('incoterm')
        shipment.transport_mode = data.get('transport_mode')
        shipment.origin_country = data.get('origin_country')
        shipment.destination_port = data.get('destination_port')
        shipment.clearing_agent_id = data.get('clearing_agent')
        shipment.ship_status = 2
        shipment.packing_list_ref = data.get('packing_list_ref')
        shipment.supplier_invoice = data.get('supplier_invoice')
        shipment.gross_weight = data.get('gross_weight', 0)
        shipment.net_weight = data.get('net_weight', 0)
        shipment.cbm = data.get('cbm', 0)
        shipment.vehicle = data.get("vehicle")

        shipment.save()

        phase_master = ShipmentPhaseMaster.objects.get(id=2)
        ShipmentPhase.objects.update_or_create(
            shipment=shipment,
            phase_code=phase_master.phase_code,
            defaults={
                'phase_name': phase_master.phase_name,
                'completed': True,
                'completed_at': timezone.now(),
                'updated_by': user,
                'order': phase_master.order,
            }
        )




        doc_type=data.get('bank_doc_type')

        if doc_type:
            bank_id = bank.b_id if hasattr(bank, 'b_id') else bank
            currency_id = currency.id if hasattr(currency, 'id') else currency
            BankDocument.objects.update_or_create(
                shipment=shipment,
                doc_type=doc_type,
                defaults={
                   
                    #'bank_id': bank if bank else None ,                # ✅ FIXED
                    'bank_id': bank_id,          # ✅ OBJECT
                    'currency_id': currency_id,
                    #'currency_id': shipment.currency_id,
                    'reference_number': data.get('reference_number'),
                   
                    'foreign_amount': shipment.amount,     # foreign
                    'amount': shipment.amount_lkr, 
                    'issue_date': _to_date(data.get('c_date')) or timezone.now().date(),
                    'due_date': _to_date(data.get('due_date')) or timezone.now().date(),
                    'company_id': shipment.company_id, 
                    'created_by': user,
                }
            )

    return shipment


############################ sales dashboard services #############################

from django.db.models import OuterRef, Subquery, IntegerField, Value, Case, When, F
from django.utils import timezone

TOTAL_PHASES = 7  # adjust if needed

def get_sales_dashboard_data():
    today = timezone.now().date()

    # 🔹 Subquery: get latest phase ORDER per shipment
    latest_phase_order = ShipmentPhase.objects.filter(
        shipment=OuterRef("pk")
    ).order_by("-order").values("order")[:1]

    # 🔹 Subquery: get latest phase NAME per shipment
    latest_phase_name = ShipmentPhase.objects.filter(
        shipment=OuterRef("pk")
    ).order_by("-order").values("phase_name")[:1]

    active_shipments = (
        Shipment.objects
        .filter(grn_complete_at_warehouse=False)
        .select_related("supplier") 
        .annotate(
            phase_order=Subquery(latest_phase_order, output_field=IntegerField()),
            current_phase=Subquery(latest_phase_name),
        )
        .annotate(
            progress=Case(
                When(phase_order__isnull=True, then=Value(0)),
                default=(F("phase_order") * 100 / TOTAL_PHASES),
                output_field=IntegerField(),
            )
        )
        .values(
            "shipment_code",
            "expected_arrival_date",
            "current_phase",
            "phase_order",
            "progress",
             "supplier__supplier_name",      
        )
        .order_by("expected_arrival_date")
    )


    

    context = {
        # ---------------- KPI CARDS ----------------
        "total_active_shipments": Shipment.objects.filter(
            grn_complete_at_warehouse=False
        ).count(),

        "new_shipment": Shipment.objects.filter(
            ship_status=1
        ).count(),

        "goods_at_port": Shipment.objects.filter(
            C_Process_Initiated=True,
            C_Process_completed=False
        ).count(),

        "on_the_way_shipment": Shipment.objects.filter(
            C_Process_completed=True,
            arrival_at_warehouse=False
        ).count(),

        "grn": Shipment.objects.filter(
            grn_upload_at_warehouse=True,
            grn_complete_at_warehouse=False
        ).count(),

        "completed_shipment": Shipment.objects.filter(
            grn_complete_at_warehouse=True
        ).count(),

        # ---------------- ACTIVE TABLE ----------------
        "active_shipments": active_shipments,
        "today": today,
    }

    return context



###################### mdi dashboard