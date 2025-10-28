from rest_framework import serializers
from .models import Shipment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ClearingAgentShipmentSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)

    class Meta:
        model = Shipment
        fields = [
            "id",
            "shipment_code",
            "supplier_name",
            "bl",
            "send_date",
            "amount",
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
            "supplier_invoice",
            "bank_doc_type",
            "assessment_document",
            "payment_marked",
            "payment_marked_date",
            "duty_paid",
            "duty_paid_date",
        ]


############################### Login

# myapp/serializers.py
# masters/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to JWT
        token['username'] = user.username
        token['groups'] = list(user.groups.values_list('name', flat=True))
        token['user_id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        data['groups'] = list(self.user.groups.values_list('name', flat=True))
        data['user_id'] = self.user.id  # 👈 Add this line
        return data

from rest_framework import serializers
from .models import Bank, Company, ItemCategory, Warehouse, Supplier, ClearingAgent

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCategory
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class ItemWarehouseOptionSerializer(serializers.Serializer):
    id = serializers.CharField()      # "itemId_warehouseId"
    label = serializers.CharField()   # "ItemName — WarehouseName"

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'  # include all fields of the Supplier model



class ClearingAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClearingAgent
        fields = '__all__'  # include all ClearingAgent fields




class arrival_notice_listSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'  # include all ClearingAgent fields


# --------------------  Shipmet list

class ShipmentSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'id',
            'bl',
            'supplier_name',
            'ship_status',
            'amount',
            'order_date',
            'container'
        ]


# -------------------- shipment phase

from .models import  ShipmentPhase

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'  # or select specific fields you need

#class ShipmentPhaseSerializer(serializers.ModelSerializer):
    #class Meta:
       # model = ShipmentPhase
        #fields = '__all__'
