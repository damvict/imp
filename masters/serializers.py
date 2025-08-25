from rest_framework import serializers
from .models import Shipment

class ClearingAgentShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            "id",
            "bank_doc_type",
            "reference_number",
        ]




################################# BankManager ##################

class BankManagerShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            "id",
            "purchase_order_no",
            "supplier_invoice",
            "bank_doc_type",
            "assessment_document",
            "send_to_clearing_agent",
            "payment_marked",
            "payment_marked_date",
        ]

######################################### MD ################

class MDShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            "id",
            "purchase_order_no",
            "supplier_invoice",
            "bank_doc_type",
            "assessment_document",
            "payment_marked",
            "payment_marked_date",
            "duty_paid",
            "duty_paid_date",
        ]