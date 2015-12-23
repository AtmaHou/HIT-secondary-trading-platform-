# -*- coding: utf-8 -*-
from django.template import Context
#from django import forms
from django.shortcuts import render_to_response
from models import *
from django import forms
from django.http import HttpResponse
from PIL import ImageFile 
import random
from django.core.mail import send_mail
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)   
    file = forms.FileField() 
    
class UploadImageForm(forms.Form):
    imagefile = forms.ImageField(required=False)    

def show_map(request):
    return render_to_response("map.html")
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
                
                c = Context({"user":user_real,"aa":1}) 
                return render_to_response("index.html", c , d)
            else:
                errors["password"] = '密码错误,请检查后重新输入！'
        else:
		 errors["email"] = '用户不存在，请点此'
    return render_to_response("login.html",{"errors":errors})

def index(request):
    want_lst = want.objects.all()    
    if "email" in request.session:
        d = Context({"products_list":Product.objects.all(),"aa":1,"want_lst":want_lst})
    else:
        d = Context({"products_list":Product.objects.all(),"want_lst":want_lst})
    
    return render_to_response("index.html", d)
    
def logout(request):
    if "email" in request.session:
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
        d = Context({"products_list":Product.objects.all(),"aa":1})
        return render_to_response("index.html",d)
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
            client = Client.objects.get(email = e)
        )
        if(post["auction"] == "yes"):
            new_product.auction = True
            new_product.auction_add = post["add_price"]
            new_product.auction_deadline = post["deadline"]
            print "yes"
        else:
            new_product.auction = False
            print "no"
            
        
        
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            new_product.image = form.cleaned_data["imagefile"]
        new_product.save()
        d = Context({"products_list":Product.objects.all(),"aa":1})
        return render_to_response("index.html",d)
    
    return render_to_response("add_product.html")  

    
def product_show(request):
    id1 = request.GET["id"]
    p = Product.objects.get(id = id1)

      
    if "email" in request.session:
        customer = Client.objects.get(email = request.session["email"])
    else:
        customer = None
	
    if request.POST:
        post = request.POST
        if "email" in request.session:
            com = Comment(content = post["text"],
                          product = p,
                          client = customer)
            com.save()
    comment_list = p.comments.all()
    if "reserved" in request.GET:
        if request.GET["reserved"] == "reserve_it":
            p.who_reserved = customer
        elif request.GET["reserved"] == 'cancle':
            p.who_reserved = None
    
    if "collected" in request.GET:
        if request.GET["collected"] == "collect_it":
            p.collected_clients.add(customer) 
        elif request.GET["collected"] == 'cancle':
            p.collected_clients.remove(customer)
    p.save()
    
    if customer:
        if not p.who_reserved: 
            reser = 0 # not reserve
        else:
            if customer == p.who_reserved:
                reser = 2 # cancle reserve
            else:
                reser = 1 # reserved
                 
        if p in customer.collect_products.all():
            collect = 1 # has been collected
        else:
            collect = 2
            
    else:
        collect = 3
        if p.who_reserved:
            reser = 1 # reserved
        else:
            reser = 3 # to login

    if datetime.now() > p.auction_deadline:
        timeout = True
    else:
        timeout = False
    msg_lst = customer.receive_msg.filter(read = False)
    want_lst = want.objects.all()
    c = Context({"p": p, "a": p.client,"c_list":comment_list,"reser":reser,"has_collected": collect,"auction":p.auction,"customer":customer,"timeout":timeout,"msg_num":len(msg_lst),"want_lst":want_lst})
    return render_to_response("productshow.html",c)

def auction(request):
    id1 = request.GET["id"]
    p = Product.objects.get(id = id1)

    if "email" in request.session:
        customer = Client.objects.get(email = request.session["email"])
    else:
        customer = None
        
    if(customer):
        flag = True
        if request.POST:
            post = request.POST
            add = float(post["price"])
            now_price = float(post["now_price"])
            now_price = now_price + add
            
            if add >= p.auction_add and now_price > p.price:
                
                flag = True
            else:
                flag = False
            if flag:
                p.price = now_price
                if p.who_reserved:
                    msg = message(content = u"您拍的商品  " + unicode(p.name) + u"  拍价已变更" + u" http://127.0.0.1:8000/product_show/?id=" + unicode(str(p.id)),
                        product = p,
                        speaker = Client.objects.get(email = "sys@sys.com"),
                        listener = p.who_reserved,
                        read = False)
                    msg.save()
                p.who_reserved = customer
                p.save()
        
    else:
        pass
    if datetime.now() > p.auction_deadline:
        timeout = True
        if p.who_reserved:
            msg = message(content = "您好，您已成功拍得商品",
                    product = p,
                    speaker = Client.objects.get(email = "sys@sys.com"),
                    listener = p.who_reserved,
                    read = False)
            msg.save()
    else:
        timeout = False
    c = Context({"p": p,"flag":flag,"custmor":customer,"timeout":timeout})
    return render_to_response("auction.html",c)

@is_online 
def bargain(request):
    id1 = request.GET["id"]
    p = Product.objects.get(id = id1)
    customer = Client.objects.get(email = request.session["email"])
    sended = False
    if request.POST:
        post = request.POST
        m = message(content = post["text"],
                    product = p,
                    speaker = customer,
                    listener = p.client,
                    read = False)
        m.save()
        sended = True
        
    c = Context({"p": p,"custmor":customer,"sended":sended})
    return render_to_response("bargain.html",c)

@is_online
def all_message(request):
    customer = Client.objects.get(email = request.session["email"])
    msg_lst = customer.receive_msg.all().order_by("-message_date")
    for m in msg_lst:
        m.read = True
        m.save()
    sended = False
    if request.POST:
        post = request.POST
        sended = True
        tmp = post["now"]
        #  post[tmp]   #表示的是这段消息
        msg = message.objects.all().get(id = tmp)
        new_msg = message(content = post[tmp],
                          product = msg.product,
                          speaker = msg.listener,
                          listener = msg.speaker,
                          read = False)
        new_msg.save()
    c = Context({"custmor":customer,"msg_lst":msg_lst,"sended":sended})
    return render_to_response("all_message.html",c)

    
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

@is_online
def my_product(request):
	e = request.session["email"]
	client = Client.objects.get(email = e)
	my_products = client.products.all()
	my_num = client.products.all().count()
	c = Context({"my_products":my_products,"my_num":my_num})
	return render_to_response("my_product.html",c)

@is_online	
def my_collection(request):
	e = request.session["email"]
	client = Client.objects.get(email = e)
	my_products = client.collect_products.all()
	my_num = my_products.count()
	c = Context({"my_collection":my_products,"collection_num":my_num})
	return render_to_response("my_collection.html",c)
	
@is_online
def delete_product(request):
	e = request.session["email"]
	client = Client.objects.get(email = e)
	id_=request.GET["id"]
	this_product=Product.objects.get(id=id_)
	this_product.delete()
	my_products = client.products.all()
	my_num = client.products.all().count()
	c = Context({"my_products":my_products,"my_num":my_num})
	return render_to_response("my_product.html",c)

@is_online
def add_collection(request):
    e = request.session["email"]
    client = Client.objects.get(email = e)
    
    id2 = request.GET["id"]
    pro = Product.objects.get(id = id2) 
    pro.collected_clients.add(client)   
    has_collected = True
        
    c = Context({"p": pro, "a": pro.client, "has_collected": has_collected})
    return render_to_response("productshow.html",c)
    
@is_online
def remove_collection(request):
    e = request.session["email"]
    client = Client.objects.get(email = e)
    
    id2 = request.GET["id"]
    pro = Product.objects.get(id = id2) 
    pro.collected_clients.remove(client)
    has_collected = False
        
    my_products = client.collect_products.all()
    my_num = my_products.count()
    c = Context({"my_collection":my_products,"collection_num":my_num})
    return render_to_response("my_collection.html",c)

def check_email(request):
    if "email" in request.session:
        usr = Client.objects.get(email = request.session["email"])
        while True:
            usr.rid = "";
            for i in range(20):
                usr.rid += str(chr(random.randint(ord('a')+1,ord('z')-1)))
            if(len(Client.objects.filter(rid = usr.rid)) == 0):
                break;
        #if failed   print str(usr.email)
        usr.save()
        send_mail('HSTP please activate your email','please click it to activate your email  http://127.0.0.1:8000/activate_email/?id='+usr.rid,'2770837735@qq.com',[usr.email],fail_silently=False)
    return render_to_response("sent_email.html")
    
def activate_email(request):
    if "id" in request.GET:
        id1 = request.GET["id"]
        if Client.objects.get(rid = id1):
            usr = Client.objects.get(rid = id1)
            vaild = True
            usr.is_identified = True
            usr.save();
        else:
            vaild = False
            
    c = Context({"vaild":vaild})
    return render_to_response("activated.html",c)
def want_show(request):
    id1 = request.GET["id"]
    w = want.objects.get(id = id1)

      
    if "email" in request.session:
        customer = Client.objects.get(email = request.session["email"])
    else:
        customer = None
	
    if request.POST:
        post = request.POST
        if "email" in request.session:
            com = Comment(content = post["text"],
                          want = w,
                          client = customer)
            com.save()
    
    comment_list = w.comments.all()
    
    for i in comment_list:
        if i.client:
            print i.client.nickname
        else:
            12345678910
    msg_lst = customer.receive_msg.filter(read = False)
    want_lst = want.objects.all()
    c = Context({"w": w, "a": w.sender,"c_list":comment_list,"customer":customer,"msg_num":len(msg_lst),"want_lst":want_lst})
    return render_to_response("want_show.html",c)


@is_online
def add_want(request):
    if request.POST:
        post = request.POST
        
        w = want(sender = Client.objects.get(email = request.session["email"]),
            content = post["text"],
            time = datetime.now())
        
        w.save()
        
    return render_to_response("add_want.html")
        
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
