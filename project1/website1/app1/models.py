from django.db import models

# Create your models here.

class Register(models.Model):
            reg_cname = models.CharField(max_length=255)
            reg_cemail = models.TextField(max_length=255)
            reg_cphone = models.CharField(max_length=255)
            reg_username = models.CharField(max_length=255)
            reg_psw = models.CharField(max_length=2)

            def __str__(self):
                return self.reg_cname
            



class Cart(models.Model):
       cart_user = models.CharField(max_length=250,default=None)
       cart_proid = models.IntegerField(null=True)
       cart_name = models.CharField(max_length=250)
       cart_price = models.FloatField(max_length=250)
       cart_image = models.FileField(null=True)
       cart_qty = models.IntegerField()
       cart_amount = models.FloatField()
       
       def __str__(self):
              return self.cart_name

class Order(models.Model):
       order_prouser = models.CharField(max_length=250,default=None)
       order_proname = models.CharField(max_length=250)
       order_proprice = models.FloatField(max_length=250)
       order_proimage = models.FileField(null=True)
       order_proqty = models.IntegerField()
       order_proamount = models.FloatField()
       order_address = models.TextField(null=True)
       order_paytype = models.CharField(null=True,max_length=10)
       order_status = models.IntegerField(default=0) 

       def __str__(self):
              return self.order_proname

class Category(models.Model):
       cat_name = models.CharField(max_length=255)
       cat_price = models.IntegerField(max_length=250,null=True)
       cat_image = models.FileField(null=True,upload_to="category")

       def __str__(self):
              return self.cat_name
       
class Product(models.Model):
    pro_name = models.CharField(max_length=250)
    pro_price = models.FloatField()
    pro_image = models.FileField(null=True,upload_to="products")
    pro_cats = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    def __str__(self):
          return self.pro_name
       
