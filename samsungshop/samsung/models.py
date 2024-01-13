from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Tv'),(2,'Mobile'),(3,'Washing Machine'),(4,'Microwave'),(5,'Air Conditioners'))
    name=models.CharField(max_length=30,verbose_name='PRODUCT_NAME')
    price=models.FloatField()
    detail=models.CharField(max_length=100,verbose_name="PRODUCT_DETAILS") #verbose_name is used for only displday
    cat=models.IntegerField(verbose_name="Category",choices=CAT)
    is_active=models.BooleanField(default=True)
    pimage=models.ImageField(upload_to='image')




    def __str__(self):
        return self.name
    


class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    cprice=models.FloatField()


class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE)
    pid=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
