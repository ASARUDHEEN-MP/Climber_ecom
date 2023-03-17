# Create your views here.

from django.conf import settings
from django.shortcuts import render,redirect
from . models import *
from hashlib import sha256
from django.contrib.auth import authenticate
from django.contrib import messages,auth 
from django.views.decorators.cache import cache_control
from category.models import Categorys,products,product_list
from admin_app.models import carosuel
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import random
from django.views.decorators.csrf import csrf_exempt,csrf_protect #Add this
from django.core.validators import EmailValidator
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
import razorpay
import smtplib
import secrets
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger





from.form import send_forget_password_mail
import uuid
# Create your views here.
@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def index(request):
    categorys = Categorys.objects.filter(status=0)
    carosuelS=carosuel.objects.get()
    paginator = Paginator(categorys,2)
    page = request.GET.get('page')
    try:
                page_data = paginator.page(page)
                
    except PageNotAnInteger:
            # If page is not an integer, display the first page.
                page_data = paginator.page(1)
                
    except EmptyPage:
            # If page is out of range, display the last page of results.
                page_data = paginator.page(paginator.num_pages)
                

    except Exception as e:
            # Handle any other exceptions that may occur.
                
                page_data = paginator.page(1)
    context={'categorys':categorys,'carosuelS':carosuelS,'page_data':page_data}
    return render(request,'user/index1.html',context)
#----------------------------------------------------------login----------------------------------
@cache_control(no_cache =True, must_revalidate =False, no_store =True)
def login(request):
    if 'username' in request.session:
        return redirect('index')
    
   
    if request.method=='POST':
        usernames=request.POST.get('username')
        password=request.POST.get('password')
        
       
        


        try:
            email=User.objects.filter(email=usernames).first()
            username=email.username
            user = authenticate(username = username,password = password)
            
            

        except:
            user = None
            pass
        if user is not None :
            auth.login(request,user)
            request.session['username']= username
            messages.info(request,'logged in successfully')
            return redirect(index)
        else:
            messages.success(request,'invalid loginrequest')
            return redirect('login')

    return render(request,'login.html')
    


#<-------------------------------------signup----------------------------->
def signup(request):
   

    
    if request.method =='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        
        if username == '':
                 messages.info(request,'username is empty')
                 return redirect(signup)
        elif email == '':
                messages.info(request,'Email is empty')
                return redirect(signup)
        elif password == '':
                messages.info(request,'password is empty')
                return redirect(signup)
        elif User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect(signup)
      
        else:
            
            message = generate_otp()
            sender_email = "asarudheen9472@gmail.com"
            receiver_email = email
            passwords = "xazwlscvvoizwvlm"
            subject = "Climber create account  OTP"
            X = message
            
            request.session['otp'] = X
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(sender_email, passwords)
            message = 'Subject: {}\n\n{}'.format(subject, message)
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
            
           
            
            request.session['names'] = username
            request.session['mails'] = email
            request.session['passwrds'] = password
           
            

            return redirect('verify_login')

    return render(request,'signup.html')






#-----------------------------------otp---------------------------------

def generate_otp(length=6):
    return ''.join(secrets.choice("0123456789") for i in range(length))


def verify_login(request):
    
    otp = request.session['otp'] 
   
    if request.method =='POST':
       
        OTP =request.POST['otp']
        
    
        if OTP == otp:
           del request.session['otp'] 
           
           
           return redirect('success')
        else:
            messages.info(request,"invalid otp") 
                  
            return redirect('verify_login')
    return render(request,'user/otp.html')


def success(request):
    username=request.session['names'] 
    email =request.session['mails'] 
    password=request.session['passwrds'] 
    
    users= User.objects.create_user(username=username,email=email,password=password)
    users.save()
    profilesave= profile.objects.create(user = users)
    profilesave.save()
    del request.session['names'] 
    del request.session['mails'] 
    del request.session['passwrds'] 
    
    return redirect('login')


    

#-------------------------------------reset password------------------
import uuid


def ChangePassword(request , token):
    context = {}
    
    
    try:
        profile_obj = profile.objects.filter(forget_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')
            
            
            
        
        
    except Exception as e:
        print(e)
    
    
    return render (request,'resetpassword/change_password.html',context)


#------------------------------userlogout---------------------------

@cache_control(no_cache = True,must_revalidate = False,no_store = True)
def user_logout(request):
    if 'username' in request.session:
        request.session.flush()
        messages.info(request,'logout successfully')
        return redirect(index)
        

#-----------------------------categry-------------------------------
def collections(request):
    categorys = Categorys.objects.filter(status=0)
    context={'categorys':categorys}
    return render(request,'categories.html',context)


#--------------------------collections------------------------------


def collection_view(request,slug):
   if(Categorys.objects.filter(slug=slug,status=0)):
      button=slug
      productt=product_list.objects.filter(category__slug=slug)
      cat_name=Categorys.objects.filter(slug=slug).first()
      categorys = Categorys.objects.filter(status=0)
      carosuelS=carosuel.objects.get()

      paginator = Paginator(productt,6)  # 10 items per page

      page = request.GET.get('page')
   
      
      try:
                page_data = paginator.page(page)
                
      except PageNotAnInteger:
            # If page is not an integer, display the first page.
                page_data = paginator.page(1)
                
      except EmptyPage:
            # If page is out of range, display the last page of results.
                page_data = paginator.page(paginator.num_pages)
                

      except Exception as e:
            # Handle any other exceptions that may occur.
                
                page_data = paginator.page(1)





      contexts = {'productt':productt,'cat_name':cat_name,'page_data':page_data,'carosuelS':carosuelS,'categorys':categorys,'button':button}
      return render(request,'user/collections_view.html',contexts)
   else:
    messages.warning(request,"no such file")
    return redirect('collections')
 #-----------------------------------All products-------------------------------------------------------

def allproducts(request):
    productt=product_list.objects.all()
    carosuelS=carosuel.objects.get()
    categorys = Categorys.objects.filter(status=0)
    
    
    paginator = Paginator(productt,6) 
    page = request.GET.get('page')
    try:
                page_data = paginator.page(page)
                print(page_data,'try')
    except PageNotAnInteger:
            # If page is not an integer, display the first page.
                page_data = paginator.page(1)
                print(page_data,'except1')
    except EmptyPage:
            # If page is out of range, display the last page of results.
                page_data = paginator.page(paginator.num_pages)
                print(page_data,'except2')

    except Exception as e:
            # Handle any other exceptions that may occur.
                print(f"An error occurred: {e}")
                page_data = paginator.page(1)
    contexts = {'productt':productt,'page_data':page_data,'carosuelS':carosuelS,'categorys':categorys,}
    return render(request,'user/collections_view.html',contexts)
#-------------------------------------single productdetails----------------------------------------------
@login_required(login_url='login')
def product_view(request,cate_slug,prod_slug):
    if(Categorys.objects.filter(slug=cate_slug,status=0)):
         if(product_list.objects.filter(slug=prod_slug,status=0)):
            product=product_list.objects.filter(slug=prod_slug,status=0).first
            context={'product':product}
            
    


         else:
           
            return redirect('collections')


    else:
        
        return redirect('collections')
   
    return render(request,'user/single_product.html',context)



#---------------------------------------cart managment ---------------------------------------------------------------------
def addtocart(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            dd=request.user
            prod_id=int(request.POST.get('product_id'))
            product_check= product_list.objects.get(id=prod_id)
            
            total=product_check.price
            
            

            if(product_check):
                    if(carts.objects.filter(user=request.user.id,product_id=prod_id)):
                        return JsonResponse({'status':"product already in cart"})

                
                
                 
                    prod_qty=int(request.POST.get('product_qty'))
                    grand=total*prod_qty
                    
                    
                    if product_check.quantity >= prod_qty:
                        dd = request.user

                        
                        carts.objects.create(user=dd,product_id=prod_id,product_qty=prod_qty,total=grand)
                        wishlists=wishlist.objects.filter(product=prod_id)
    
                        wishlists.delete()
                        return JsonResponse({'status':"product added successfully"})
                    else:
                        return JsonResponse({'status':"only "+str(product_check.quantity)+"quantity available"})


            else:
                return JsonResponse({'status':"no such product found"})

             

        else:
            return JsonResponse({'status':"login to continue"})
    return redirect('index')

@login_required(login_url='login')
def cart(request):
    dd = request.user
    total=0
    user_profile = UserProfilepic.objects.filter(user=request.user)
    
    
    counter=0
    cart_items = carts.objects.filter(user = dd)

    for item in cart_items:
        total +=item.total
        counter += 1
       
        
    
        

    
    

    context={'cart_items':cart_items,'total':total,'counter':counter,'user_profile':user_profile}
    
    return render(request,'user/cartview.html',context)



def delete_cart(request,id):
    my=carts.objects.get(id=id)
    my.delete()
    return redirect('cart')

def updatecart(request):
    if request.method=='POST':
        prod_id=int(request.POST.get('product_id'))
        product_check= product_list.objects.get(id=prod_id)
        total=product_check.price
        userss=request.user
        users_id=request.user.id
        if(carts.objects.filter(user_id=userss,product_id=prod_id)):
            prod_qty=int(request.POST.get('product_qty'))
            cart=carts.objects.get(user_id=users_id,product_id=prod_id)
            grand=total*prod_qty
            cart.product_qty=prod_qty
            cart.total=grand
            cart.save()
            return JsonResponse({'status':"update successfull"})
        
        return redirect('index')

#checkout----------------------------------
def checkout(request):
    user = request.user
    total=0
    grand_total = 0
    dd=request.user
    discount = 0
    button=0
    
    
    addrssz=userdetails.objects.filter(is_default=True,user=request.user)
    cartitems=carts.objects.filter(user=dd)
    address=userdetails.objects.filter(user=dd)
    for item in address:
        button=item.fname

    for item in cartitems:
        total +=item.product.price * item.product_qty
    
    if 'coupons' in request.session:
        coupons=request.session['coupons']
        coup = coupon.objects.get(coupon_code=coupons)
        coupss=coup.coupon_code
        discount = coup.discount
        messages.info(request,'')
        Used_Coupon.objects.create(user = user,coupon = coup )
    coupen=coupon.objects.all()
    m=total
    grand_total += total-discount
    
    context={'cartitems':cartitems,'grand_total':grand_total,'address':address,'addrssz':addrssz,'discount':discount,'m':m,'coupen':coupen,'button':button}
    return render(request,'user/usercheckout.html',context)







#--------------------------------------------------------------userdetails----------------
def userdetail(request):
    d=request.user
    idss=request.user.id
    users = User.objects.get(username=d)
    address=userdetails.objects.filter(user=idss)
    dp=UserProfilepic.objects.filter(user=request.user).first
    context={'users':users,'address':address,'dp':dp}
    return render(request,'user/userdetails.html',context)


def addaddress(request):
    d=request.user
    users = User.objects.get(username=d)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        country = request.POST['country']
        city = request.POST['city']
        pincode = request.POST['pincode']
        user = users
        hh=len(phone)
        if hh!=10:
            messages.info(request,"enter 10 digit number for phonenumber ")
            return redirect('addaddress')
    
        else:
            newaddress=userdetails.objects.create( fname = fname,
                                               lname=lname,
                                               email = email,
                                               phone=phone,
                                               address=address,
                                               state = state,
                                               city =city,
                                               pincode=pincode,
                                               country=country,
                                               user=user)
            newaddress.save()
       
        return redirect(userdetail)
           

        
        
        
    

    return render(request,'user/addaddress.html')

def delete_address(request,pk):
    address=userdetails.objects.get(id=pk)
    address.delete()
    return redirect(userdetail)

def edit_address(request,pk):
    address=userdetails.objects.get(id=pk)
    dd=request.user
    userz=User.objects.get(username=dd)
    context={'userz':userz,
       'address':address
    }
    if request.method == 'POST':
       address.fname = request.POST['fname']
       address. lname = request.POST['lname']
       address.email = request.POST['email']
       address.phone = request.POST['phone']
       address.state = request.POST['state']
       address.country = request.POST['country']
       address.city = request.POST['city']
       address.pincode = request.POST['pincode']
       address.address = request.POST['address']

       address.save()
       return redirect(userdetail)
    return render(request,'user/editaddress.html',context)    
from django.db.models import Q
def test(request):
    ued=Used_Coupon.objects.filter(user=request.user)
    
    return render(request,'test.html')


#addess set up for order----
def default(request,id):
    dd=request.user
    address=userdetails.objects.filter(user=dd)
    defaultaddress=userdetails.objects.get(id=id)
    defaultaddress.is_default=True
    defaultaddress.save()
    
    for i in address:
        if i != defaultaddress:
            i.is_default=False
            i.save()
            

    return redirect('checkout')


#placeorder------

def cashondelivery(request):
    
    return render(request,'pay/cash.html')

@csrf_exempt #This skips csrf validation. Use csrf_protect to have validation
def placeorder(request):

    total=0
    coupons=0
    discount=0
    button=0
    coup=0
    cart_total_price = 0
    dd=request.user
    payment_mod='cod'
    payment_id='none'
    cart_ids=carts.objects.filter(user=request.user)
    tracking_no =( random.randint(100000,999999))
    
    
        
    
       
    if 'coupons' in request.session:
        coupons=request.session['coupons']
        coup = coupon.objects.get(coupon_code=coupons)
        discount = coup.discount
        del request.session['coupons']

    
    
     
    
    for item in cart_ids:
           cart_total_price +=item.product.price * item.product_qty
    cart_total_price -=discount
    orders = order.objects.create(
       user=request.user,
       total_price=cart_total_price,
       address=userdetails.objects.get(is_default=True,user=request.user),
       tracking_no=tracking_no,
       payment_mode=payment_mod,
       payment_id=payment_id,
       status='Confirmed',
       discountprice=discount,
       
    )
    orders.save()
    grandtotals =sucessamount.objects.create(
        user=request.user,
        grandtotal=cart_total_price
    )
    
    grandtotals.save()
    for item in cart_ids:
        total=item.product.price*item.product_qty

        ordersitem = orderitem.objects.create(
                user=request.user,
                orderit=orders,
                product=item.product,
                price=item.product.price,
                quantity=item.product_qty,
                total=total,

                
                    )
        ordersitem.save()
    
    #dcsrc quantiy from admin stock
    for item in cart_ids:
        productz=product_list.objects.filter(id=item.product_id).first()
        productz.quantity=productz.quantity-item.product_qty
        productz.save()
    cart_ids.delete()
    
    
    return redirect('orderview')
    

#-----------------------------------------show myorder--------------------------
def refund(request):
    tr_id=request.session['tracking_no'] 
    
    ord=order.objects.filter(tracking_no=tr_id).filter(user=request.user).first()
    if ord.payment_mode == 'razorpay':
            paymentid=ord.payment_id
            amount=ord.total_price
            client = razorpay.Client(auth=('rzp_test_Q76eqQekpYrXb6','YVThyYWz0AaRdOYxnhukMJ01'))
            refund_amount = int(amount) * 100
            response = client.payment.refund(paymentid, refund_amount)
            status='refund'
            ord.status=status
            ord.save()
            
            return redirect(cancelsuccess)
    else:
         return redirect(cancelsuccess)
    # return render(request,'test.html',context)
def refundsuccess(request):
     return render(request,'orders/refund.html')
     


def cancelsuccess(request):
        tr_id=request.session['tracking_no'] 
        del request.session['tracking_no'] 
        ord=order.objects.filter(tracking_no=tr_id).filter(user=request.user).first()
        amount=ord.total_price
        payment_mode=ord.payment_mode
        return render(request,'orders/usercancel.html',{'amount':amount,'payment_mode':payment_mode})

def orderview(request):
    u=request.user
    total=0
    oderz=order.objects.filter(user=u).order_by('-id')

   
    
    ff={
        'oderz':oderz,
        
    }
    return render(request,'orders/orderview.html',ff)


def vieworder(request,tr_id):
    total=0
    
    ord=order.objects.filter(tracking_no=tr_id).filter(user=request.user).first()
    ord_itm=orderitem.objects.filter(orderit=ord)
    for item in ord_itm:
        total+=item.total
        
   
    delivered=ord.status=='Delivered'    
   
    button=ord.payment_mode
    
    
 
    context={'ord':ord,'ord_itm':ord_itm,'delivered':delivered,'total':total,'button':button}
    
    return render(request,'orders/userorderview.html',context)



def cancelorders(request,pk):
    if request.user.is_authenticated:
        orders=order.objects.get(id=pk)
        ord=order.objects.filter(id=pk).first()
        orders.status = 'Cancelled'
        orders.save()
        ord_itm=orderitem.objects.filter(orderit=orders.id)
        for i in ord_itm:
             i.status = 'Cancelled'
             i.save()
        request.session['tracking_no']= ord.tracking_no
        return redirect(refund)
    

def orderdel(request):
    ords=order.objects.filter(user=request.user).first()
    if ords.status == 'Cancelled':
        ords.delete()
    return redirect('orderview')

    
@csrf_exempt
def pay(request):
    return redirect('/')

#test
@csrf_exempt
def my_orders(request):

    usr=sucessamount.objects.filter(user=request.user)
    for item in usr:
      total=item.grandtotal
    usr.delete() 
    
    
    
    
        
        
    context={'total':total}
    
    return render(request,'pay/sucess.page.html',context)



#-------------------------coupon-----------------------------------------------
def applycoupon(request):
    if request.method == 'POST':
        coupons=request.POST.get("coupon")
        ued=Used_Coupon.objects.filter(user=request.user)
        coup=coupon.objects.filter(coupon_code=coupons).first()
        
        for item in ued:
             if item.coupon.coupon_code == coupons:
                   used=True
             else:
                  used=False
        
        if used == True:
             messages.info(request,' coupon is used')
             return redirect('checkout')
             
        else:   
           if coup:
            
            request.session['coupons'] = coupons
            return redirect("checkout")
           else:
            messages.info(request,'invalid coupon')
            return redirect("checkout")
                 
#--------------------------search---------------------------------------------#
def productlistsajax(request):
    serch=product_list.objects.filter(status=0).values_list('name',flat=True)
    prdctlist=list(serch)
    return JsonResponse(prdctlist,safe=False)

def serach_prdct(request):
    if request.method == 'POST':
        searchtest=request.POST['srchbarprdt']
        if searchtest=="":
           return redirect(request.META.get('HTTP_REFERER'))
        else:
            product=product_list.objects.filter(name__contains=searchtest).first()
            if product:
                return redirect('collections/'+product.category.slug+'/'+product.slug)
            else:
                messages.info(request,'Product NOT FOUND')
                return redirect(request.META.get('HTTP_REFERER'))
 
    return redirect(request.META.get('HTTP_REFERER'))



#--------------------------about----------------------------------------------
def about(request):
    carosuelS=carosuel.objects.get()
    context={'carosuelS':carosuelS}

    return render(request,'user/About.us.html',context)

#-----------------------pdfdownload-----------------------------------------------

class GenerateOrderInvoicePDF(View):
    def get(self, request, *args, **kwargs):
        # Get order from ID in URL parameters
    
        order_id = kwargs.get('order_id')
        
        ord=order.objects.filter(tracking_no=order_id).filter(user=request.user).first()
        orders=orderitem.objects.filter(orderit=ord)
        
        
        # Render HTML template with order data
        context = {'orders': orders,'ord':ord
                   }
        template = get_template('orders/user_invoice.html')
        html = template.render(context)

        # Create PDF response
        pdf = HttpResponse(content_type='application/pdf')
        pdf['Content-Disposition'] = f'attachment; filename="order_{order_id}_invoice.pdf"'

        # Generate PDF from HTML
        pisa_status = pisa.CreatePDF(html, dest=pdf)
        if pisa_status.err:
            return HttpResponse('Error generating PDF')

        return pdf

#------------------------------razorpay-----------------------------------------
from django.conf import settings
def payit(request):
    if request.method == 'POST':
        payment_mod= request.POST.get('payment_mode')
        total=int(request.POST.get('total'))
        phone=request.POST.get('phone')
        name=request.POST.get('name')
       
       
        client = razorpay.Client(auth=('rzp_test_Q76eqQekpYrXb6','YVThyYWz0AaRdOYxnhukMJ01'))

        DATA = {
            "amount": total * 100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        payment = client.order.create(data=DATA)
        context={
            'payment_mod':payment_mod,
            'total':total,
            'phone':phone,'name':name,
            'id' :str( payment['id']),
             
        }
        
        return render(request,'pay/payit.html',context)
  
#-------------------------------razorpayverification--------------------------------
@csrf_exempt 
def verification_payment(request):
    total=0
    discount=0
    
    cart_total_price = 0
    payment_id= request.POST.get('razorpay_payment_id','')
    cart_total_price = 0
    
    payment_mod='razorpay'
   
    dd_id=request.user.id
    cart_ids=carts.objects.filter(user=dd_id)
    tracking_no =( random.randint(100000,999999))
    if 'coupons' in request.session:
        coupons=request.session['coupons']
        del request.session['coupons']
        coup = coupon.objects.get(coupon_code=coupons)
        discount = coup.discount
        
    for item in cart_ids:
        total+=item.product.price*item.product_qty
        

    total -=discount
   
    orders = order.objects.create(
       user=request.user,
       total_price=total,
       address=userdetails.objects.get(is_default=True,user=request.user),
       tracking_no=tracking_no,
       payment_mode=payment_mod,
       payment_id=payment_id,
       status='Confirmed',
       discountprice=discount,
    )
    orders.save()
    grandtotals =sucessamount.objects.create(
        user=request.user,
        grandtotal=total
    )
    grandtotals.save()
    for item in cart_ids:
        total =item.product.price*item.product_qty
       
    
    for item in cart_ids:

        ordersitem = orderitem.objects.create(
                user=request.user,
                orderit=orders,
                product=item.product,
                price=item.product.price,
                quantity=item.product_qty,
                total=item.total,
                    )
        ordersitem.save()
    productz=product_list.objects.filter(id=item.product_id).first()
    productz.quantity=productz.quantity-item.product_qty
    productz.save()
    cart_ids.delete()
    return redirect(my_orders)
        

    

        
    

   

#----------------------------changepassword---------------------------- 
def changepassword(request):
    
    if request.method == 'POST':
            newpassword = request.POST.get('new_password')
            repassword = request.POST.get('reconfirm_password')
            user=request.user
            if user is  None:
                  messages.success(request, 'No user id found.')
                  return redirect('login')
            
            if  newpassword != repassword:
                   messages.success(request, 'both should  be equal.')
                   return redirect('changepassword')
            else:
                print(user)
                print("helooooo")
                userid=request.user.id
                user_obj=User.objects.get(id=userid)
                user_obj.set_password(newpassword)
                user_obj.save()
                messages.success(request, 'password change successfull.')
                return redirect('index')

           
    
    return render(request,'resetpassword/newpassword.html')
#-------------------------forgetpassword-------------------------------
def ForgetPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email=request.POST.get('email')
    
        if User.objects.filter(username=username,email=email).first():
               
                message =generate_otp()
                sender_email = "asarudheen9472@gmail.com"
                receiver_email = email
                subject = "Reset Password OTP"
                passwords = "xazwlscvvoizwvlm" 
                X = message
                request.session['otp'] = X
            
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(sender_email, passwords)
                message = 'Subject: {}\n\n{}'.format(subject, message)
                server.sendmail(sender_email, receiver_email, message)
                server.quit()
                request.session['name'] = username
                
                

                return redirect('password_otp')
                
        else:
             messages.success(request, 'Not user found with this username and email.')
             return redirect('forget_password')

    
    
    
            
    
        
        
    return render(request,'resetpassword/forget_password.html')


#----------------------------passwordotp----------------------------------
def password_otp(request):
    otp = request.session['otp'] 
    
    if request.method =='POST':
       
        OTP =request.POST['otp']
        print(OTP)
    
        if OTP == otp:
           del request.session['otp'] 
           
           
           return redirect('repassword')
        else:
            messages.info(request,"invalid otp") 
    return render(request,'resetpassword/password_verification.html')

def repassword(request):
    if request.method == 'POST':
            newpassword = request.POST.get('new_password')
            repassword = request.POST.get('reconfirm_password')
            
            if  newpassword != repassword:
                   messages.success(request, 'both should  be equal.')
                   return redirect('repassword')
            else:
                usernames= request.session['name']
                del request.session['name']
                print(usernames)
                print('heljfdsodh')
                user_obj=User.objects.get(username=usernames)
                user_obj.set_password(newpassword)
                user_obj.save()
                
                messages.success(request, 'password change successfull.')
                return redirect('index')
            

    
    
    
    return render(request,'resetpassword/newpassword.html') 


def returns(request,tr_id):
   ord=order.objects.filter(tracking_no=tr_id).filter(user=request.user).first()
   total=ord.total_price
   grandtotal=total-ord.discountprice
   print(ord.discountprice)
   wallets=userwallets.objects.create( user = request.user,
    
        walletamount=grandtotal
    )
   wallets.save()
    
   if  ord.status =='Delivered':
        ord.status='Returned'
        
   ord.save()
   
    
    
    
    
   return redirect('orderview')

def placeaddaddress(request):
    d=request.user
    users = User.objects.get(username=d)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        country = request.POST['country']
        city = request.POST['city']
        pincode = request.POST['pincode']
        user = users
        hh=len(phone)
        if hh!=10:
            messages.info(request,"enter 10 digit number for phonenumber ")
            return redirect('addaddress')
    
        else:
            newaddress=userdetails.objects.create( fname = fname,
                                               lname=lname,
                                               email = email,
                                               phone=phone,
                                               address=address,
                                               state = state,
                                               city =city,
                                               pincode=pincode,
                                               country=country,
                                               user=user)
            newaddress.save()
       
        return redirect(checkout)
    return render(request,'user/addnewaddress.html')

#-----------------------------wishlist---------------------------------------
def wishlists(request):
    wishlists=wishlist.objects.filter(user=request.user)
    context={'wishlists':wishlists}
    return render(request,'wishlist/wishlist.html',context)

def addwishlist(request):
    
    if request.method=='POST':
        if request.user.is_authenticated:
            dd=request.user
            prod_id=int(request.POST.get('product_id'))
            product_check= product_list.objects.get(id=prod_id)
            
            if(product_check):
                if(wishlist.objects.filter(user=request.user.id,product_id=prod_id)):
                        return JsonResponse({'status':"product already in wishlist"})
                else:
                    wishlist.objects.create(user=request.user,product_id=prod_id)
                    return JsonResponse({'status':"product added in successfully"})
            
            
            else:
                return JsonResponse({'status':"no such product found"})
    
    
    
        else:
            return JsonResponse({'status':"login to continue"})
    return redirect('index')



def delete_wishlist(request,id):
    wishlists=wishlist.objects.get(id=id)
    
    wishlists.delete()
    return redirect('wishlists')
#-------------------------------------------profile-----------------------
def edit_profile(request):
    try:
        user_profile = UserProfilepic.objects.get(user=request.user)
    except UserProfilepic.DoesNotExist:
        user_profile = UserProfilepic(user=request.user)

    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        messages.success(request, 'Profile picture updated successfully.')
        return redirect('userdetails')

    return render(request, 'user/edit_profile.html', {'user_profile': user_profile})

def delete_profile_picture(request):
   user_profile = UserProfilepic.objects.filter(user=request.user.id).first()
   print(user_profile)
   user_profile.delete()
   return redirect('userdetails')
#---------------------------------userprofile---------------------------
def wallets(request):
    amount=0
    total=0
    grandtotal=0
    orders=userwallets.objects.filter(user=request.user)
    for item in orders:
       total += item.walletamount
       amount=total
       
    return render(request,'pay/wallets.html',{'amount':amount})

def walletamount(request):
    payment_mod='Wallet amount'
    payment_id='none'
    cart_total_price=0
    discount=0
    total=0
    
    wallet=userwallets.objects.filter(user=request.user)
    
    walletamount=0
    cart_ids=carts.objects.filter(user=request.user)
    for item in cart_ids:
           cart_total_price +=item.product.price * item.product_qty
    
    tracking_no =( random.randint(100000,999999))
    if 'coupons' in request.session:
        coupons=request.session['coupons']
        coup = coupon.objects.get(coupon_code=coupons)
        discount = coup.discount
        del request.session['coupons']
        
          


    cart_total_price -= discount
    
    for item in wallet:
        
       walletamount = item.walletamount
    
    
    grandtotal = float(walletamount)-float(cart_total_price)
    
    
    
    
    
    if cart_total_price <= walletamount:
                orders = order.objects.create(
                user=request.user,
                total_price=cart_total_price,
                address=userdetails.objects.get(is_default=True,user=request.user),
                tracking_no=tracking_no,
                payment_mode=payment_mod,
                payment_id=payment_id,
                status='Confirmed',
                discountprice=discount,
                
                )
                orders.save()
                grandtotals =sucessamount.objects.create(
                user=request.user,
                grandtotal=cart_total_price
                )
    
                grandtotals.save()
                for item in cart_ids:
                    total=item.product.price*item.product_qty

                    ordersitem = orderitem.objects.create(
                            user=request.user,
                            orderit=orders,
                            product=item.product,
                            price=item.product.price,
                            quantity=item.product_qty,
                            total=total,

                            
                                )
                    ordersitem.save()
                for item in cart_ids:
                    productz=product_list.objects.filter(id=item.product_id).first()
                    productz.quantity=productz.quantity-item.product_qty
                    productz.save()
                cart_ids.delete()
                
                
                wallet=userwallets.objects.filter(user=request.user)
                for item in wallet:
                    item.walletamount=grandtotal
                    item.save()
                
                
                return redirect('my_orders')
    else:
        messages.info(request,'Wallet has insufficent balance')
        return redirect('checkout')
                
                    
        

    
    
    
    