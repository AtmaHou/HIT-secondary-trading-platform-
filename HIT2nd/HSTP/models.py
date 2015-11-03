from django.db import models
from django.utils import timezone
import re
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core import validators
# Create your models here.
class Client(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField(primary_key=True,unique=True,
                              validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')]) #only tag
    password = models.CharField(max_length=6)    #!!!
    realname = models.CharField(max_length=30,blank=True)
    nickname = models.CharField(max_length=30,blank=True)
    #date_joined    register_date = models.DateTimeField(default=datetime.now())  #auto    
    IDcard = models.IntegerField(max_length=18,blank=True)       #IDcard
    studentID = models.IntegerField(max_length=10,blank=True) #!!!
    colledge = models.CharField(max_length=50,blank=True)
    school = models.CharField(max_length=50,blank=True)
    major = models.CharField(max_length=50,blank=True)
    grade = models.CharField(max_length=50,blank=True)
    telephone = models.IntegerField(max_length=15,blank=True)   #!!!
    sex = models.BooleanField(blank=True)
    is_identified = models.BooleanField(blank=True)
    seller_level = models.IntegerField(default=1)    #auto
    buyer_level = models.IntegerField(default=1)    #auto
    is_lonly_dog = models.BooleanField(blank=True)
    is_online = models.BooleanField(default=False)

class Product(models.Model):
    productID = models.DateTimeField(primary_key=True,unique=True,default=timezone.now)   #only tag 20151101220616
    name = models.CharField(max_length=80)     
    price = models.FloatField()   #!!!
    client = models.ForeignKey(Client,related_name="products")        
    trading_place = models.CharField(max_length=80)  
    is_identified = models.BooleanField(default=False)
    introduction = models.CharField(max_length=200) 
    is_reserved = models.BooleanField(default=False)
    collected_clients = models.ManyToManyField(Client,related_name="collect_products")
    
class Comment(models.Model):
    product = models.ForeignKey(Product,primary_key=True,related_name="comments")  
    client = models.ForeignKey(Client,related_name="comments")    #comment man
    content = models.CharField(max_length=200) 
    comment_date = models.DateTimeField(default=timezone.now) 
    
class Category(models.Model):
    product = models.ForeignKey(Product,primary_key=True,related_name="categories")   
    category = models.CharField(max_length=40)     #type
    

class Label(models.Model):
    product = models.ForeignKey(Product,max_length=14,primary_key=True,related_name="labels")    
    label = models.CharField(max_length=40)    #tag

class Image(models.Model):
    image = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')

    