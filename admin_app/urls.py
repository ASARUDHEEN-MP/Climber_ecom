from django.urls import path
from . import views


urlpatterns = [
   path ('',views.adminlogin,name='adminlogin'),
   path ('adminpanel',views.adminpanel,name='adminpanel'),
   path ('logout',views.logout,name='logout'),
   path('user_mgmt',views.user_mgmt,name='user_mgmt'),
   path('blockuser/<int:pk>',views.block_user,name='block_user'),
   path('unblockuser/<int:id>',views.unblock_user,name='unblock_user'),
   path('adminpanel',views.admindashboard,name='admindashboard'),
   path('delete/<int:id>',views.delete,name='delete'),
 

   #categories
   path('category',views.view_category,name='view_category'),
   path('deletes/<int:id>',views.deletes,name='deletes'),
   path('updatecatgory/<int:pk>',views.updatecatgory,name='updatecatgory'),
   path('addcategory',views.addcategory,name='add_category'),

   #collection
   path('collection_list',views.collection_list,name='collection_list'),
   path('add_collection',views.addProduct,name='add_collection'),
   path('updateProduct/<int:pk>/', views.updateProduct, name='updateProduct'),
   path('deletesss/<int:id>',views.deletesss,name='deletesss'),


   #carousel
    path('view_carousel',views.view_carousel,name='view_carousel'),
    path('add_carousel',views.add_carousel,name='add_carousel'),
    path('update_carousel/<int:pk>',views.update_carousel,name='update_carousel'),
#orders
path('orders',views.orders,name='orders'),
path('ordstatus/<int:id>',views.ordstatus,name="ordstatus"),
path('canclorder/<int:id>',views.canclorder,name="canclorder"),
path('deleteord/<int:id>',views.deleteord,name="deleteord"),
path('vieworders/<str:tr_id>',views.vieworders,name="vieworders"),
 #couponlist
path('couponlist',views.couponlist,name="couponlist"),
path('addcoupon',views.addcoupon,name="addcoupon"),
path('activecp/<int:pk>',views.activecp,name="activecp"),
path('deactivecp/<int:id>',views.deactivecp,name="deactivecp"),
path('deletecp/<int:id>',views.deletecp,name="deletecp"),
path('canceledorders',views.canceledorders,name="canceledorders"),
#chartview--------------------
path('chart',views.chart, name='chart'),

path('filterchart',views.filterchart,name="filterchart"),
#sales report
path('excel_sales_report',views.excel_sales_report,name="excel_sales_report"),
path('SalesReport',views.SalesReport,name="SalesReport"),
path('pdf_dwnld',views.pdf_dwnld,name="pdf_dwnld"),
]