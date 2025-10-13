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
from .models import Bank, Company, ItemCategory, Warehouse

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
