from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control

from category.models import Categorys,products,product_list
from . models import carosuel
from django.contrib import messages 
from django.contrib.auth.models import User
from user_app.models import *
from . forms import ProductForm,categoryForm,orderForm,carosuelForm
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from openpyxl import Workbook
from django.http.response import JsonResponse
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q




# Create your views here.
def admindashboard(request):
    return render(request,'admindashboard.html')


@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def adminlogin(request):
    if 'user' in request.session:
        return redirect(adminpanel)
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password=password)
        if user is not None:
           if  user.is_superuser:
                request.session['user'] = username
                return redirect(adminpanel)
        else:
            messages.info(request,'you are not an admin')
            return redirect(adminlogin)
    
            
        
    return render(request,'adminlogin.html') 

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def adminpanel(request):
    
    return render(request,'admin_templates/admin_dashboard.html')

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def logout(request):
    if 'user' in request.session:
        request.session.flush()
    return redirect(adminlogin)


#usermanagment------
def user_mgmt(request):
    users = User.objects.filter(is_superuser=False)
    
    return render(request,'admin_templates/usermanagment.html',{'users':users})






def block_user(request,pk):
    user = User.objects.get(id =pk)
    user.is_active = False
    user.save()
    print('user blocked')
    return redirect('user_mgmt')

def unblock_user(request,id):
    user = User.objects.get(id= id)
    user.is_active  = True
    user.save()
    print('user is active')
    return redirect('user_mgmt')
 
def delete(request,id):
    my=User.objects.get(id=id)
    my.delete()
    return redirect('user_mgmt')






#------------------------categories----------------------------------------------
def view_category(request):
    category = Categorys.objects.all()
    return render(request,'admin_templates/category.html',{'category':category})

def deletes(request,id):
    pop=Categorys.objects.get(id=id)
    pop.delete()
    return redirect('view_category')


def addcategory(request):
    form = categoryForm()

    if request.method == 'POST':
        form = categoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_category')
    else:
        form = categoryForm()

    context = {
        "form":form
    }

    return render(request, 'admin_templates/add_category.html', context)



def updatecatgory(request,pk):
    Category = Categorys.objects.get(id=pk)
    
    form = categoryForm(instance=Category)

    if request.method == 'POST':
        form = categoryForm(request.POST, request.FILES, instance=Category)
        if form.is_valid():
            form.save()
            return redirect('collection_list')

    context = {
        "form":form
    }

    return render(request, 'admin_templates/update_product.html', context)


#----------------------------------PRODUCT collection---------------------------------

def collection_list(request):
    product = product_list.objects.all()
    return render(request,'admin_templates/collection_list.html',{'product':product})

def addProduct(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('collection_list')
    else:
        form = ProductForm()

    context = {
        "form":form
    }

    return render(request, 'admin_templates/add_collection.html', context)
    

def updateProduct(request,pk):
    product = product_list.objects.get(id=pk)
    
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_category')

    context = {
        "form":form
    }

    return render(request, 'admin_templates/update_category.html', context)


 
def deletesss(request,id):
    my=product_list.objects.get(id=id)
    my.delete()
    return redirect('collection_list')



#carousel
def view_carousel(request):
    product = carosuel.objects.all()
    return render(request,'admin_templates/carouel_list.html',{'product':product}
    )

def add_carousel(request):
    form = carosuelForm()

    if request.method == 'POST':
        form = carosuelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_carousel')
    else:
        form = carosuelForm()

    context = {
        "form":form
    }

    return render(request, 'admin_templates/add_carousel.html', context)




def update_carousel(request,pk):
    carosuels = carosuel.objects.get(id=pk)
    
    form = carosuelForm(instance=carosuels)

    if request.method == 'POST':
        form = carosuelForm(request.POST, request.FILES, instance=carosuels)
        if form.is_valid():
            form.save()
            return redirect('view_category')

    context = {
        "form":form
    }

    return render(request, 'admin_templates/update_category.html', context)

#------------------------------------order-------------------------------------------------------------------------------------------
def orders(request):
    ord=order.objects.all()
    return render(request,'admin_templates/orderllist.html',{"ord":ord})

def ordstatus(request,id):
    ord=order.objects.get(id=id)
    if  ord.status =='Confirmed':
        ord.status='Shipped'
    elif ord.status =='Shipped':
         ord.status='Out_for_delivery'
    elif ord.status =='Out_for_delivery':
         ord.status='Delivered'
    
    ord.save()
    print(ord)
    return redirect('orders')

def canclorder(request,id):
    ord=order.objects.get(id=id)
    ord.status='Cancelled'
    ord.save()
    return redirect('orders')

def deleteord(request,id):
    ord=order.objects.get(id=id)
    ord.delete()
    return redirect('orders')


def vieworders(request,tr_id):
    total=0
    ord=order.objects.filter(tracking_no=tr_id).filter(user=request.user).first()
    ord_itm=orderitem.objects.filter(orderit=ord)
    for item in ord_itm:
        total+=item.total
   
    
    
 
    context={'ord':ord,'ord_itm':ord_itm,'total':total}
    
    return render(request,'admin_templates/orderview.html',context)
    
 
def canceledorders(request):
    ord=order.objects.filter(status='Cancelled')
    context={'ord':ord}
    
    return render(request,'orders/cancelorder.html',context)
    

#---------------------------------------------coupon--------------------------------------------------------------

def couponlist(request):
    coup=coupon.objects.all()
    return render(request,'admin_templates/couponview.html',{'coup':coup})

def addcoupon(request):
    form = orderForm()

    if request.method == 'POST':
        form = orderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('couponlist')
    else:
        form = orderForm()

    context = {
        "form":form
    }

    return render(request, 'admin_templates/add_coupon.html', context)
    
    
def activecp(request,pk):
    coup=coupon.objects.get(id=pk)
    print(coup)
    coup.is_active =True
    coup.save()
    return redirect('couponlist')

def deactivecp(request,id):
    coup=coupon.objects.get(id=id)
    coup.is_active =False
    coup.save()
    return redirect('couponlist')

def deletecp(request,id):
    coup=coupon.objects.get(id=id)
    coup.delete()
    return redirect('couponlist')



#-------------------------------------------------------chart------------------------
def chart(request):
    user=User.objects.all().count()   
    ordercount=order.objects.all().count() 
    orderlist=orderitem.objects.all()
    orderlists = orderitem.objects.filter(Q(orderit__status ='Delivered'))
    Grandtotal=0
    for item in orderlists:
    
        total=item.orderit.total_price
        Grandtotal=+total+Grandtotal
    product = []
    qty = []
    
    for items in orderlist:
        if items.product.name in product:
            index = product.index(items.product.name)
            qty[index] += items.quantity

        else:
            product.append(items.product.name)
            qty.append(items.quantity)

  
    context = {
        'product':product,
        "qty":qty,
        'Grandtotal':Grandtotal,
        'user':user,
        'ordercount':ordercount,
    }
    return render(request,'orders/chart.html',context)
    
def filterchart(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
       
        
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    
    orderlist = orderitem.objects.filter(Q(orderit__status ='Confirmed') & Q(orderit__created_at__date__gte = start_date) & Q(orderit__created_at__date__lte = end_date))
   
    product = []
    qty = []
    
    for items in orderlist:
        if items.product.name in product:
            index = product.index(items.product.name)
            qty[index] += items.quantity

        else:
            product.append(items.product.name)
            qty.append(items.quantity)

 
    data = {
        'product':product,
        "qty":qty,
    }

    return JsonResponse(data)


#-----------------------salesReport--------------------------------------------------
def SalesReport(request):
    total=0
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        

    
        
        if start_date_str is not None:
            start_date = datetime.strptime(start_date_str,  '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
          
            orderitemlist = orderitem.objects.filter(Q(orderit__status ='Delivered') & Q(orderit__created_at__date__gte = start_date) & Q(orderit__created_at__date__lte = end_date))
           
        else:
             orderitemlist = orderitem.objects.filter(Q(orderit__status ='Delivered') )
        
           
      
    
    
    Grandtotal=0
    for item in orderitemlist:
    
        total=item.orderit.total_price
        Grandtotal=+total+Grandtotal
        
        
    context={'orderitemlist':orderitemlist,'Grandtotal':Grandtotal,'total':total}
    return render(request,'orders/salesreport.html',context)

def excel_sales_report(request):
    month=timezone.now().month
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
    sales_data=[
        ['Date','product','quantity','price','Total'],
    ]
    if start_date_str is not None:
              start_date = datetime.strptime(start_date_str,  '%Y-%m-%d')
              end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
              orders = orderitem.objects.filter(Q(orderit__status ='Delivered') & Q(orderit__created_at__date__gte = start_date) & Q(orderit__created_at__date__lte = end_date))
    else:
            orders = orderitem.objects.filter(Q(orderit__status ='Delivered'))

    for order in orders:
        sales_data.append([
            # order.orderit.order.id,
            order.orderit.created_at.strftime('%m/%d/%Y %I:%M %p'),
            order.product.name,
            order.quantity,
            order.price,
            order.orderit.total_price



        ])
    wb = Workbook()
    ws= wb.active
    ws.title='sales Report'
    for row in sales_data:
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'
    wb.save(response)
    return response

def pdf_dwnld(request):
    if request.method == 'GET':
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
    if start_date_str is not None:
            start_date = datetime.strptime(start_date_str,  '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            orders = orderitem.objects.filter(Q(orderit__status ='Delivered') & Q(orderit__created_at__date__gte = start_date) & Q(orderit__created_at__date__lte = end_date))
    else:
         orders = orderitem.objects.filter(Q(orderit__status ='Delivered'))


    # for item in orders:
    #        date= item.orderit.created_at.strftime('%m/%d/%Y %I:%M %p'),
    #        product= item.product.name,
    #        quantity= item.quantity,
    #        price=item.price,
    #        totalprice=item.orderit.total_price
    Grandtotal=0
    for item in orders:
    
        total=item.orderit.total_price
        Grandtotal=+total+Grandtotal
    context={'orders':orders,'Grandtotal':Grandtotal}
    
    template = get_template('orders/admin_salesreport.html')
    html = template.render(context)
    pdf = HttpResponse(content_type='application/pdf')
    pdf['Content-Disposition'] = f'attachment; filename="order_{"sales report"}_invoice.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=pdf)
    if pisa_status.err:
           return HttpResponse('Error generating PDF')

    return pdf




