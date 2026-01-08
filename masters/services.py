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
        shipment.currency_id = (currency.id if hasattr(currency, 'id') else currency)
        shipment.amount = data.get('amount')           # foreign amount
        shipment.amount_lkr = data.get('amount_lkr') 
        shipment.c_date = _to_date(data.get('due_date'))
        shipment.expected_arrival_date = (
        _to_date(data.get('expected_arrival_date'))
        or shipment.expected_arrival_date
    )
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
            BankDocument.objects.update_or_create(
                shipment=shipment,
                doc_type=doc_type,
                defaults={
                    #'bank': data.get('bank'),
                    'bank_id': bank, 
                    'currency_id': shipment.currency_id, 
                    'reference_number': data.get('reference_number'),
                    'currency': shipment.currency,
                    'foreign_amount': shipment.amount,     # foreign
                    'amount': shipment.amount_lkr, 
                    'issue_date': _to_date(data.get('c_date')) or timezone.now().date(),
                    'due_date': _to_date(data.get('due_date')) or timezone.now().date(),
                    'company_id': shipment.company_id, 
                    'created_by': user,
                }
            )

    return shipment
