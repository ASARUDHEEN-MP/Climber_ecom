from django.db import models

# Create your models here.
class Categorys(models.Model):
    category_name = models.CharField(max_length=50,null=True,blank=False)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=150,null=False,blank=False)
    image = models.ImageField(upload_to='categories' ,default='',null=True)
    status=models.BooleanField(default=False,help_text="0=default,1=Hidden")
    
    

    
   
    def __str__(self):
        
        return self.category_name

class products(models.Model):
    image = models.ImageField(upload_to='products',null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE, default=False, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=1)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    slug = models.CharField(max_length=140, default='SOME STRING',null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=Hidden")
    quantity = models.IntegerField(default=0)
   

    def __str__(self):
        return self.name
    

class product_list(models.Model):
    image = models.ImageField(upload_to='products',null=False, blank=False)
    image1 = models.ImageField(upload_to='products',null=False, blank=False)
    image2 = models.ImageField(upload_to='products',null=False, blank=False)
    image3 = models.ImageField(upload_to='products',null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE, default=False, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=6)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    slug = models.CharField(max_length=140, default='SOME STRING',null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=Hidden")
    quantity = models.IntegerField(default=0)
   

    def __str__(self):
        return self.name
    
class MultipleImage(models.Model):
    images = models.FileField()