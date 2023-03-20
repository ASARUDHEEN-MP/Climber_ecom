from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(profile)
admin.site.register(order)
admin.site.register(carts)
admin.site.register(orderitem)
admin.site.register(coupon)
admin.site.register(sucessamount)
admin.site.register(Used_Coupon)
admin.site.register(userwallets)



