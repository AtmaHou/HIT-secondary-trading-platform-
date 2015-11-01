from django.db import models
import datetime
# Create your models here.
class Client(models.Model):
    email = models.EmailField(primary_key=True,unique=True) #唯一标识
    password = models.IntegerField()    #!!!
    realname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)
    register_date = models.DateTimeField(default=datetime.now)  #自动生成    
    IDcard = models.IntegerField(max_length=18)       #身份证号
    studentID = models.IntegerField(max_length=10) #!!!
    colledge = models.CharField(max_length=50)
    school = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    telephone = models.IntegerField(max_length=15)   #!!!
    sex = models.BooleanField(default=True)
    is_identified = models.BooleanField(default=False)
    seller_level = models.IntegerField(default=1)    #自动生成1 
    buyer_level = models.IntegerField(default=1)    #自动生成1 
    is_lonly_dog = models.BooleanField(default=True)

class Product(models.Model):
    productID = models.DateTimeField(primary_key=True,unique=True,default=datetime.now)   #唯一标识  上架日期 20151101220616
    name = models.CharField(max_length=80)     
    price = models.FloatField()   #!!!
    client = models.ForeignKey(Client,related_name="products")        #识别卖家
    trading_place = models.CharField(max_length=80)  
    is_identified = models.BooleanField(default=False)
    introduction = models.CharField(max_length=200) 
    is_reserved = models.BooleanField(default=False)
    collected_clients = models.ManyToMany(Client,related_name="collect_products")
    
class Comment(models.Model):
    product = models.ForeignKey(Product,primary_key=True,related_name="comments")  #商品
    client = models.ForeignKey(Client,related_name="comments")    #评论者
    content = models.CharField(max_length=200) 
    comment_date = models.DateTimeField(default=datetime.now) 
    
class Category(models.Model):
    product = models.ForeignKey(Product,primary_key=True,related_name="categories")    #识别商品
    category = models.CharField(max_length=40)     #商品类别
    

class Label(models.Model):
    product = models.ForeignKey(Product,max_length=14,primary_key=True,related_name="labels")    #识别商品
    label = models.CharField(max_length=40)    #商品标签
    