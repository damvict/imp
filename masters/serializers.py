from rest_framework import serializers
from .models import Shipment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum  # <-- import Sum


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
            "packing_list_ref",
            "send_date",
            "send_to_clearing_agent_payment",
            "payref_document",
           

        ]






################################# BankManager ##################

class BankManagerShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            "id",
            "shipment_code",
            "supplier_invoice",
            "bank_doc_type",
            "assessment_document",
            "send_to_clearing_agent",
            "payment_marked",
            "payment_marked_date",
            "duty_paid_bank",    # NEW
            "payment_type",      # NEW
            "pay_note", 
        ]



class BankManagerpaySerializer(serializers.ModelSerializer):
   #supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    class Meta:
        model = Shipment
        fields = [
            "id",
            "shipment_code",
            "vessel",           
            "total_duty_value",
            "duty_paid_date",
           
        ]


class BankManagerpayrefSerializer(serializers.ModelSerializer):
   #supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    class Meta:
        model = Shipment
        fields = [
            "id",
            "shipment_code",
            "vessel",           
            "total_duty_value",
            "duty_paid_date",
            "send_to_clearing_agent_payment_date",
            "payref_document_ref",
            "payref_document"
           
        ]

######################################### MD ################



class MDShipmentSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
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
            "shipment_code",
            "vessel",
            "duty_paid_bank",
            "supplier_name",
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

###  ##!!!!!!!!!!  class ShipmentSerializer(serializers.ModelSerializer):
    
    ###  ##!!!!!!!!!!supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
   ###  ##!!!!!!!!!! amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

   ###  ##!!!!!!!!!! class Meta:
       ###  ##!!!!!!!!!! model = Shipment
       ###  ##!!!!!!!!!! fields = [
         ###  ##!!!!!!!!!!   'id',
         ###  ##!!!!!!!!!!   'bl',
         ###  ##!!!!!!!!!!   'supplier_name',
         ###  ##!!!!!!!!!!   'ship_status',
          ###  ##!!!!!!!!!!  'amount',
         ###  ##!!!!!!!!!!   'order_date',
         ###  ##!!!!!!!!!!   'container',
        ###  ##!!!!!!!!!!    'shipment_code',
      ###  ##!!!!!!!!!!  ]



# -------------------- shipment phase

from .models import ShipmentDispatch

class ShipmentDispatchSerializer_type2(serializers.ModelSerializer):
   
    class Meta:
        model = ShipmentDispatch
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at"]

from .models import  ShipmentPhase

class ShipmentSerializer(serializers.ModelSerializer):
    dispatch = ShipmentDispatchSerializer_type2(read_only=True)
       
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    class Meta:
        model = Shipment
        fields = '__all__'  # or select specific fields you need

#class ShipmentPhaseSerializer(serializers.ModelSerializer):
    #class Meta:
       # model = ShipmentPhase
        #fields = '__all__'



#------------------------------ Shipment dispatch

from .models import ShipmentDispatch

class ShipmentDispatchSerializer(serializers.ModelSerializer):
    shipment_code = serializers.CharField(source='shipment.shipment_code', read_only=True)
    class Meta:
        model = ShipmentDispatch
        fields = "__all__"
        read_only_fields = ["created_by", "created_at", "updated_at"]



#################### Bank settlement

from .models import BankDocument, Settlement

class BankDocumentSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='shipment.company.name', read_only=True)
    customer = serializers.CharField(source='shipment.supplier.name', read_only=True)  # optional if you want supplier/customer name

    class Meta:
        model = BankDocument
        fields = [
            'id',
            'reference_number',
            'customer',       # supplier/customer
            'company_name',   # new
            'amount',           
            'issue_date',
            'due_date',
            'settled',
            'settlement_date',
            'doc_type',
            'bank_id',
            'converted_to_imp',
            'imp_reference',
            'created_by',
            'created_at',
            
        ]



class SettlementSerializer(serializers.ModelSerializer):
    document_details = BankDocumentSerializer(source='document', read_only=True)

    class Meta:
        model = Settlement
        fields = '__all__'



