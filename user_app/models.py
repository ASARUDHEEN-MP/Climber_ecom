from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from datetime import datetime
from django.contrib.auth.models import User
from category.models import product_list


# Create your models here.



    


    

class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    
    

    



class carts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product_list, on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    
#userdetails
class userdetails(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   fname=models.CharField(max_length=150,null=False)
   lname=models.CharField(max_length=150,null=False)
   phone=models.CharField(max_length=150,null=False)
   email=models.CharField(max_length=150,null=False)
   address=models.TextField(null=False)
   state=models.CharField(max_length=150,null=False)
   country=models.CharField(max_length=150,null=False)
   city=models.CharField(max_length=150,null=False)
   pincode=models.CharField(max_length=150,null=False)
   is_default=models.BooleanField(default=False)


class order(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    address =models.ForeignKey(userdetails,on_delete=models.CASCADE)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=250,null=False)
    payment_id=models.CharField(max_length=250,null=True)
    STATUS = (
         ('Out_for_delivery','Out_for_delivery'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Pending','Pending'),
       
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned')
    )
    status  =   models.CharField(max_length=30, choices=STATUS, default='pending')
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=150,null=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return '{}-{}'.format(self.id,self.tracking_no)

class orderitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderit =models.ForeignKey(order,on_delete=models.CASCADE)
    product =models.ForeignKey(product_list,on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quantity=models.IntegerField(null=False)

    def __str__(self) :
        return '{}-{}'.format(self.order.id,self.order.tracking_no)

class test(models.Model):
    address =models.ForeignKey(userdetails,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class coupon(models.Model):
    coupon_code = models.CharField(max_length=50,blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=6)
    is_active =models.BooleanField(default=True)
    

class Used_Coupon(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    coupon = models.ForeignKey(coupon,on_delete=models.CASCADE,null=True)






