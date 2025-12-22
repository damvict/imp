from django.urls import path
#from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import (
    WarehouseListView, WarehouseCreateView,
    WarehouseUpdateView, WarehouseDeleteView
)

from .views import (
    CompanyListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView
)

from django.conf import settings
from django.conf.urls.static import static
from .views import upload_assessment_document

from .views import (
    BankListView,
    BankCreateView,
    BankUpdateView,
    BankDeleteView,
)

from .views import bank_dashboard
from .views import bank_doc_types
from .views import incoterms
from .views import transport_modes
from .views import shipment_types
from .views import confirm_handover

from .views import ShipmentDispatchCreateView

from masters.views import confirm_handover


from .views import (
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
)

from .views import (
    ClearingAgentListView,
    ClearingAgentCreateView,
    ClearingAgentUpdateView,
    ClearingAgentDeleteView
)


from .views import shipment_detail_api

from .views import record_grn_upload
from .views import get_next_shipment_code
from .views import bank_documents_summary
from .views import clearing_agent_users

urlpatterns = [
    # Item Category URLs
    path('itemcategory/', views.itemcategory_list, name='itemcategory_list'),
    path('itemcategory/create/', views.itemcategory_create, name='itemcategory_create'),
    path('itemcategory/edit/<int:pk>/', views.itemcategory_edit, name='itemcategory_edit'),
    path('itemcategory/delete/<int:pk>/', views.itemcategory_delete, name='itemcategory_delete'),


     # Vehicle Type URLs
    path('vehicletypes/', views.vehicle_type_list, name='vehicle_type_list'),
    path('vehicletypes/create/', views.vehicle_type_create, name='vehicle_type_create'),
    path('vehicletypes/edit/<int:pk>/', views.vehicle_type_edit, name='vehicle_type_edit'),
    path('vehicletypes/delete/<int:pk>/', views.vehicle_type_delete, name='vehicle_type_delete'),

    #### status colour
    path('statuscolors/', views.status_color_list, name='status_color_list'),
    path('statuscolors/create/', views.status_color_create, name='status_color_create'),
    path('statuscolors/edit/<int:pk>/', views.status_color_edit, name='status_color_edit'),
    path('statuscolors/delete/<int:pk>/', views.status_color_delete, name='status_color_delete'),

    path('salesdivisions/', views.salesdivision_list, name='salesdivision_list'),
    path('salesdivisions/create/', views.salesdivision_create, name='salesdivision_create'),
    path('salesdivisions/edit/<int:pk>/', views.salesdivision_edit, name='salesdivision_edit'),
    path('salesdivisions/delete/<int:pk>/', views.salesdivision_delete, name='salesdivision_delete'),
    
    path('companies/', CompanyListView.as_view(), name='company_list'),
    path('companies/create/', CompanyCreateView.as_view(), name='company_create'),
    path('companies/<int:pk>/edit/', CompanyUpdateView.as_view(), name='company_edit'),
    path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),
    #path('companies/', CompanyListView.as_view(), name='company_list'),
    #path('companies/add/', CompanyCreateView.as_view(), name='company_add'),
    #path('companies/<int:pk>/edit/', CompanyUpdateView.as_view(), name='company_edit'),
    #path('companies/<int:pk>/delete/', CompanyDeleteView.as_view(), name='company_delete'),

    path('suppliers/', SupplierListView.as_view(), name='supplier_list'),
    path('suppliers/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('suppliers/<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('suppliers/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),


    path('clearingagents/', ClearingAgentListView.as_view(), name='clearingagent_list'),
    path('clearingagents/add/', ClearingAgentCreateView.as_view(), name='clearingagent_add'),
    path('clearingagents/<int:pk>/edit/', ClearingAgentUpdateView.as_view(), name='clearingagent_edit'),
    path('clearingagents/<int:pk>/delete/', ClearingAgentDeleteView.as_view(), name='clearingagent_delete'),


    path('shipments/', views.shipment_list, name='shipment_list'),
    path('shipments/create/', views.shipment_create, name='shipment_create'),
    path('shipment/edit/<int:pk>/', views.shipment_edit, name='shipment_edit'),
    path('shipment/delete/<int:pk>/', views.shipment_delete, name='shipment_delete'),

    path('bank-controller/', views.bank_controller_view, name='bank_controller_view'),
    #path('bank-controller/update/<int:shipment_id>/', views.bank_controller_update, name='bank_controller_update'),
    path("bank-controller/update/<int:shipment_id>/bank-update/", views.bank_controller_update, name="bank_controller_update"),

    ##path("shipments/<int:shipment_id>/bank-update/", views.bank_controller_update, name="bank_controller_update"),
    #path("shipments/<int:shipment_id>/bank-mupdate/", views.bank_manager_update, name="bank_manager_update"),

    ###bank_controller_view


    #bank MAmager
     path('bank-manager/', views.bank_manager_view, name='bank_manager_view'),
     path("bank-manager/update/<int:shipment_id>/bank-update/", views.bank_manager_update, name="bank_manager_update"),



    path('shipments/pending-arrival/', views.pending_arrival_list, name='pending_arrival_list'),
    path('shipments/details/<int:detail_id>/arrival-update/',views.arrival_update_detail,name='arrival_update_detail'),
    
    path('shipments/pending-unloading/', views.pending_unloading_list, name='pending_unloading_list'),
    path('shipments/start-unloading/<int:pk>/', views.start_unloading, name='start_unloading'),
    
    ############## unloading completed
    path('shipments/complete-unloading/', views.unloading_in_progress_list, name='unloading_in_progress_list'),
    path('shipments/finish_unloading/<int:pk>/', views.finish_unloading, name='finish_unloading'),


    path('clearing-agent/shipments/', views.clearing_agent_shipments_view, name='clearing_agent_shipments_view'),
    path('clearing-agent/upload/<int:shipment_id>/', views.upload_assessment_document_view, name='upload_assessment_document_view'),
    
    ######################################### 
    
    path('warehouses/', WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/create/', WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouses/update/<int:pk>/', WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouses/delete/<int:pk>/', WarehouseDeleteView.as_view(), name='warehouse_delete'),


    path('shipments/admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('reports/average-unloading-time/', views.average_unloading_time_report, name='average_unloading_time_report'),
    path('shipments/warehouse-dashboard/', views.warehouse_dashboard, name='warehouse_dashboard'),
    path('shipments/md-dashboard/', views.md_dashboard, name='md_dashboard'),
    path("shipments/approve-duty/<int:shipment_id>/", views.approve_duty_paid_md, name="approve_duty_paid_md"),


    path("reports/stage-times/", views.shipment_stage_times_report, name="shipment_stage_times_report"),
    path('reports/stage-times/pdf/', views.shipment_stage_times_report_pdf, name='shipment_stage_times_report_pdf'),

    


    path('users/create/', views.create_user, name='create_user'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/change_password/', views.change_user_password, name='change_user_password'),

    path('api/shipments/clearing-agent/', views.clearing_agent_shipments, name='clearing_agent_shipments'),
    ###path("api/shipments/<int:shipment_id>/upload/", views.upload_assessment_document, name="upload_assessment_document"),
    path('api/upload-assessment/<int:shipment_id>/', views.upload_assessment_document, name='upload_assessment_document'),
    path('api/C_Process_Initiated/<int:shipment_id>/', views.C_Process_Initiated, name='C_Process_Initiated'),
    path('api/shipments/dispatch/', views.clearing_agent_dispatch, name='clearing_agent_dispatch'),
    path('api/truck/arrivals/', views.truck_arrivals, name='truck_arrivals'),
    path('api/grn/record/', views.grn_record, name='grn_record'),
    path('api/grn/confirm/', views.grn_confirm, name='grn_confirm'),

    path('api/record_arrival/<int:shipment_id>/', views.record_arrival, name='record_arrival'),
    path('api/record_departure/<int:shipment_id>/', views.record_departure, name='record_departure'),
    path('api/record_grn_upload/<int:shipment_id>/', views.record_grn_upload, name='record_grn_upload'),
    path('api/record_grn_confirm/<int:shipment_id>/', views.record_grn_confirm, name='record_grn_confirm'),


    
    
    path('api/bank_manager/mark_payment/<int:shipment_id>/', views.mark_payment_done, name='mark_payment_done'),
    path('api/bank_manager/payment_ref/', views.bank_manager_payment_reference, name='bank_manager_payment_reference'),
    path('api/bank_manager/bm_update_payment_ref/<int:shipment_id>/', views.bm_update_payment_ref, name='bm_update_payment_ref'),


    

    path('api/md/shipments/', views.md_shipments, name='md_shipments'),
    path('api/md/approve_duty/<int:shipment_id>/', views.approve_duty_paid, name='approve_duty_paid'),


    path('md/banks/', views.md_bank_dashboard, name='md_bank_dashboard'),


    ##############    bank #############
    path('banks/', BankListView.as_view(), name='bank_list'),
    path('banks/create/', BankCreateView.as_view(), name='bank_create'),
    path('banks/<int:pk>/update/', BankUpdateView.as_view(), name='bank_update'),
    path('banks/<int:pk>/delete/', BankDeleteView.as_view(), name='bank_delete'),


    ####### enf of Bank ########
    ####################### API #############################
    path('api/bank-dashboard/', bank_dashboard, name='bank_dashboard'),
    path('api/dashboard/', views.dashboard_view, name='dashboard'),
    path('api/shipments/next-code/', get_next_shipment_code),

    path('api/shipment-create/', views.shipment_create_api, name='shipment-create-api'), 

    path('api/banks/', views.banks_list, name='banks-list'),
    path('api/companies/', views.companies_list, name='companies-list'),
    path('api/items/', views.items_list, name='items_list'),
    path('api/warehouses/', views.warehouses_list, name='warehouses-list'),
    path('api/bank-doc-types/', bank_doc_types, name='bank-doc-types'),
    path('api/incoterms/', incoterms, name='incoterms'),
    path('api/transport-modes/', transport_modes, name='transport-modes'),
    path('api/shipment-types/', shipment_types, name='shipment-types'),
    path('api/item-warehouse-options/', views.item_warehouse_options, name='item-warehouse-options'),
    path('api/bank-controller-shipments/', views.bank_controller_shipments, name='bank_controller_shipments'),
    path('api/confirm-handover/<int:shipment_id>/', confirm_handover, name='confirm-handover'),
    path('api/suppliers/', views.suppliers_list, name='suppliers_list'),
    path('api/clearingagents/', views.clearing_agents_list, name='clearing_agents_list'),
    path('api/arrival_notice/', views.arrival_notice_list, name='arrival_notice_list'),
    path('api/ca_pay_uploaded/', views.clearing_agent_shipments_pay_uploaded, name='clearing_agent_shipments_pay_uploaded'),
    path("clearing-agent-users/", clearing_agent_users),

    path('api/bank-manager/', views.bank_manager_shipments_initiate, name='bank_manager_shipments_initiate'),
    path('api/bank-manager/update/<int:shipment_id>/', views.bank_manager_update, name='bank_manager_update'),

    path('api/shipment-phase/<int:shipment_id>/', shipment_detail_api, name='shipment-detail'),
    path('api/shipment-list/', views.shipment_list, name='shipment-list'),


    ############ Dispatch
     path("api/dispatch/<int:shipment_id>/", ShipmentDispatchCreateView.as_view(), name="shipment-dispatch"),


      path('api/shipments/clearing-agent-summary/', views.clearing_agent_summary, name='clearing-agent-summary'),



     # Bank Document & Settlement APIs
path('api/bank-documents/', views.bank_documents_list, name='bank_documents_list'),
path('api/bank-documents/<int:pk>/', views.bank_document_detail, name='bank_document_detail'),
 path('api/bank-summary/', bank_documents_summary, name='bank_documents_summary'),

path('api/settlements/', views.settlements_list, name='settlements_list'),
path('api/settlements/<int:pk>/', views.settlement_detail, name='settlement_detail'), 

]       


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




