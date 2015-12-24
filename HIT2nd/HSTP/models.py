# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
# -*- coding: utf-8 -*-
import re
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from datetime import *
# Create your models here.
    
class Client(models.Model):
    email = models.EmailField(primary_key=True,unique=True,
                              validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')]) #only tag
    password = models.CharField(max_length=6)    #!!!
    realname = models.CharField(max_length=30,blank=True,null=True)
    nickname = models.CharField(max_length=30,default="匿名",blank=True,null=True)
    register_date = models.DateTimeField(default=timezone.now)  #auto 
    IDcard = models.CharField(max_length=18,blank=True,null=True)       #IDcard
    studentID = models.IntegerField(max_length=10,default=0) #!!!
    colledge = models.CharField(max_length=50,blank=True,null=True)
    school = models.CharField(max_length=50,blank=True,null=True)
    major = models.CharField(max_length=50,blank=True,null=True)
    grade = models.CharField(max_length=50,blank=True,null=True)
    telephone = models.CharField(max_length=15,blank=True,null=True)   #!!!
    sex = models.BooleanField(blank=True)
    is_identified = models.BooleanField(blank=False)
    seller_level = models.IntegerField(default=1)    #auto
    seller_products_count = models.IntegerField(default=0)
    buyer_level = models.IntegerField(default=1)    #auto
    buyer_products_count = models.IntegerField(default=0)
    is_lonly_dog = models.BooleanField(blank=True)
    is_online = models.BooleanField(blank=True)
    image = models.ImageField(upload_to='client/images', blank=True,null=True)
    rid = models.CharField(max_length=20,blank=True)

class Booth(models.Model):
    client = models.ForeignKey(Client,related_name="booths",primary_key=True,unique=True)
    booth_name = models.TextField(max_length=20,blank=True,null=True)    
    lat = models.FloatField()
    lng = models.FloatField()
    address = models.TextField(max_length=50,blank=True,null=True) 
    introduction  = models.TextField(max_length=500,blank=True,null=True) 
    show_date = models.TextField(max_length=50,blank=True,null=True) 
    
class Product(models.Model):
    add_time = models.DateTimeField(unique=True,default=timezone.now)   #only tag 20151101220616
    name = models.CharField(max_length=80)     
    price = models.FloatField() 
    client = models.ForeignKey(Client,related_name="products")        
    trading_place = models.CharField(max_length=80)  
    is_identified = models.BooleanField(default=False)
    introduction = models.TextField(max_length=500,blank=True,null=True) 
    is_reserved = models.BooleanField(default=False)
    collected_clients = models.ManyToManyField(Client,related_name="collect_products")
    image = models.ImageField(upload_to='product/images', blank=True,null=True)
    who_reserved = models.ForeignKey(Client,related_name="reserved_products",blank=True,null=True)
    auction = models.BooleanField(default=False)
    auction_add = models.FloatField(default=0)
    auction_deadline = models.DateTimeField(default=datetime(2050,1,1,0,0,0))
    view_count = models.IntegerField(default=0)
    category = models.CharField(max_length=20)
    which_booth = models.ForeignKey(Booth,related_name="products",blank=True,null=True)
	
class want(models.Model):
    sender = models.ForeignKey(Client,related_name="want_msg")
    content = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    
class Comment(models.Model):
    product = models.ForeignKey(Product,related_name="comments",null=True) 
    client = models.ForeignKey(Client,related_name="comments")    #comment man
    content = models.CharField(max_length=200) 
    comment_date = models.DateTimeField(default=timezone.now)
    want = models.ForeignKey(want,related_name="comments",null=True)
    
class Category(models.Model):
    product = models.ForeignKey(Product,primary_key=True,related_name="categories")   
    category = models.CharField(max_length=40)     #type
    



    
class message(models.Model):
    speaker = models.ForeignKey(Client,related_name="send_msg")
    listener = models.ForeignKey(Client,related_name="receive_msg")
    content = models.CharField(max_length=200)
    message_date = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(Product,related_name="msg")
    read = models.BooleanField(default=False)

    

