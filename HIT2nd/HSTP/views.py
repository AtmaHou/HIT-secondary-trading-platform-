# -*- coding: utf-8 -*-
from django.template import Context
#from django import forms
from django.shortcuts import render_to_response
from models import *
from django import forms
from django.http import HttpResponse
import ImageFile 

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)   
    file = forms.FileField() 
    
class UploadImageForm(forms.Form):
    imagefile = forms.ImageField(required=False)    
    
def register(request):
    flag = -1
    if request.POST:
        post = request.POST
        new_client = Client(
          email = post["email"],
          password = post["password"])
        password2 = post["password2"]
        password = post["password"]
        l = len(Client.objects.filter(email = post["email"]))
          #验证密码是否相同以及Email是否注册过
        if (password == password2) and (l == 0):
            new_client.save()
            flag = 1#可以通过
        elif(password != password2) and (l == 0):
            flag = 2#密码错误
        elif(l != 0):
            flag = 3#邮箱已经被注册
    if flag == 1:
        return render_to_response("login.html")
    else:
        c = Context({"flag":flag})
        return render_to_response("register.html",c)
def login(request):
    errors = {"email":"","password":""}
    d = Context({"products_list":Product.objects.all()})
    if request.POST:
        post = request.POST
        user = Client.objects.filter(email = post["email"])
        if len(user):
            user_real = Client.objects.get(email = post["email"])
            if user_real.password == post["password"]:
                request.session["email"] = user_real.email
                c = Context({"user":user_real}) 
                return render_to_response("index2.html", c , d)
            else:
                errors["password"] = '密码错误,请检查后重新输入！'
        else:
		 errors["email"] = '用户不存在，请点此'
    return render_to_response("login.html",{"errors":errors})

def index(request):
    d = Context({"products_list":Product.objects.all()})
    return render_to_response("index.html", d)
    
def logout(request):
    del request.session["email"]
    d = Context({"products_list":Product.objects.all()})
    return render_to_response("index.html",d)
def is_online(fn):
    def check(request,*args):																												
        if "email" in request.session:
            return fn(request,*args)
        else:
            return render_to_response("login.html")
    return check	
    
def return_login(request):
    return render_to_response("login.html")
def return_index(request):
    d = Context({"products_list":Product.objects.all()})
    return render_to_response("index.html",d)

@is_online
def finish_user(request):
    e = request.session["email"]
    client = Client.objects.get(email = e)

    if request.POST:
        post = request.POST
        client.studnetID = post["studentID"]
        client.IDcard = post["IDcard"]
        client.telephone = post["telephone"]
        client.realname = post["realname"]
        client.nickname = post["nickname"]
        client.major = post["major"]
        client.grade = post["grade"]
        client.sex = post["sex"]
        client.is_lonly_dog = post["is_lonly_dog"]
        
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            client.image = form.cleaned_data["imagefile"]
        
        client.save()
        d = Context({"products_list":Product.objects.all()})
        return render_to_response("index2.html",d)
    a = Context({"client":client})     
    return render_to_response("add_inf.html",a)

def search_product(request):
    if request.POST:
        post = request.POST
        search = post["search_product"]
        if Product.objects.filter(name__contains=search):
            d = Context({"products_list":Product.objects.filter(name__contains=search)})
            return render_to_response("search_product.html", d)           
        return render_to_response("search_product.html") 

@is_online
def add_product(request):
    e = request.session["email"] 
    if request.POST:
        post = request.POST
        new_product = Product(
            name = post["name"],
            price = post["price"],
            trading_place = post["trading_place"],
            introduction = post["introduction"],
            client = Client.objects.get(email = e),
        )        
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            new_product.image = form.cleaned_data["imagefile"]
        new_product.save()
        d = Context({"products_list":Product.objects.all()})
        return render_to_response("index2.html",d)
    
    return render_to_response("add_product.html")  

def product_show(request):
    id1 = request.GET["id"]
    p = Product.objects.get(id = id1)
    c = Context({"p": p, "a": p.client})
    return render_to_response("productshow.html",c)

@is_online    
def seller_inf(request):
    e = request.GET["email"]
    client = Client.objects.get(email = e)
    c = Context({"client":client})
    return render_to_response("seller_inf.html",c)

@is_online        
def user_inf(request):
    e = request.session["email"] 
    client = Client.objects.get(email = e)
    c = Context({"client":client})
    return render_to_response("user_inf.html",c)
    
#    return render_to_response("productshow.html")
    
#def search_product(request):
#    if request.POST:
#        post = request.POST
#        search = post["search_product"]
#        all_product = Product.objects.all()
#        for product in all_product:
#            if search in product.name
#        if People.objects.filter(name = search_name):
#            d = Context({"people_list":People.objects.filter(name = search_name)})
#            return render_to_response("search_people.html", d)
#        else:
#            return render_to_response("none_search_people.html") 
#def addPicture(request):  
#    if request.method == 'POST':  
#        form = UploadImageForm(request.POST, request.FILES)  
#        if form.is_valid():  
#            f = request.FILES["imagefile"]  
#            parser = ImageFile.Parser()  
#            for chunk in f.chunks():  
#                parser.feed(chunk)  
#            img = parser.close()  
#            # 在img被保存之前，可以进行图片的各种操作，在各种操作完成后，在进行一次写操作  
#            img.save()

#class UserForm(forms.Form):
#    email = forms.EmailField(required=False,label='email:')
#    password = forms.CharField(required=False,max_length=6,label='password:',widget=forms.PasswordInput())

#def register(request):
#    if request.method == 'POST':
#        uf = UserForm(request.POST)
#        if uf.is_valid():
#            email = uf.cleaned_data['email']
#            password = uf.cleaned_data['password']
#            
#            client = Client()
#            client.email = email
#            client.password = password
#            client.save()
#            return HttpResponseRedirect("/login/")
#    else:
#        uf = UserForm()
#    return render_to_response("html/register.html", {
#        'uf': uf,
#    })