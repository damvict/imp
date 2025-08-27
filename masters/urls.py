from django.urls import path
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


    path('shipments/', views.shipment_list, name='shipment_list'),
    path('shipments/create/', views.shipment_create, name='shipment_create'),
    path('shipment/edit/<int:pk>/', views.shipment_edit, name='shipment_edit'),
    path('shipment/delete/<int:pk>/', views.shipment_delete, name='shipment_delete'),
    path("shipments/<int:shipment_id>/bank-update/", views.bank_controller_update, name="bank_controller_update"),
    
    path('shipments/pending-arrival/', views.pending_arrival_list, name='pending_arrival_list'),
    path('shipments/details/<int:detail_id>/arrival-update/',views.arrival_update_detail,name='arrival_update_detail'),
    
    path('shipments/pending-unloading/', views.pending_unloading_list, name='pending_unloading_list'),
    path('shipments/start-unloading/<int:pk>/', views.start_unloading, name='start_unloading'),
    
    ############## unloading completed
    path('shipments/complete-unloading/', views.unloading_in_progress_list, name='unloading_in_progress_list'),
    path('shipments/finish_unloading/<int:pk>/', views.finish_unloading, name='finish_unloading'),
    
    
    path('warehouses/', WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/create/', WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouses/update/<int:pk>/', WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouses/delete/<int:pk>/', WarehouseDeleteView.as_view(), name='warehouse_delete'),


    path('shipments/admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('reports/average-unloading-time/', views.average_unloading_time_report, name='average_unloading_time_report'),
    path('shipments/warehouse-dashboard/', views.warehouse_dashboard, name='warehouse_dashboard'),
    path('shipments/md-dashboard/', views.md_dashboard, name='md_dashboard'),
    path("shipments/approve-duty/<int:shipment_id>/", views.approve_duty_paid_md, name="approve_duty_paid_md"),

    path('users/create/', views.create_user, name='create_user'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<int:user_id>/change_password/', views.change_user_password, name='change_user_password'),

    path('api/shipments/clearing-agent/', views.clearing_agent_shipments, name='clearing_agent_shipments'),
    path("api/shipments/<int:shipment_id>/upload/", views.upload_assessment_document, name="upload_assessment_document"),

    path('api/bank_manager/shipments/', views.bank_manager_shipments, name='bank_manager_shipments'),
    path('api/bank_manager/mark_payment/<int:shipment_id>/', views.mark_payment_done, name='mark_payment_done'),

    path('api/md/shipments/', views.md_shipments, name='md_shipments'),
    path('api/md/approve_duty/<int:shipment_id>/', views.approve_duty_paid, name='approve_duty_paid'),
     
]       

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


