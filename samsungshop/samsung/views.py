from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from samsung.models import Product,Cart,Order
from django.db.models import Q
import random
# Create your views here.



def home(request):
    userdata=request.user.id
    # print("UserData id:",userdata)
    # print("UserData id:",request.user.is_authenticated)
    obj=Product.objects.filter(is_active=True)
    context={'product' :obj}
    return render(request,"index.html",context)






def register(request):
    if request.method=="GET":
        return render(request,'register.html')
    else:
        u=request.POST['uname']
        p=request.POST['upass']
        c=request.POST['ucpass']
        uobj=User.objects.create(username=u,email=u)
        uobj.set_password(p)
        uobj.save()
        return redirect('/register')
    

def user_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        u=request.POST['uname']
        p=request.POST['upass']
        a=authenticate(username=u,password=p)
        if a is not None:
            print(a)
            print(a.password,a.id)
            login(request,a)
            return redirect('/') #HttpResponse("login Successfull" )#
        else:
            print(a)
            return HttpResponse("Login Fail" )




def user_logout(request):
    logout(request)
    return redirect("/")




def product_detail(request,pid):
    obj=Product.objects.filter(id=pid)
    context={'product':obj}
    return render(request,'productdetail.html',context)





def catfilter(request,cv):
    if cv == '1':
        obj=Product.objects.filter(cat=1)
        context={'product':obj}
        return render(request,'index.html',context)
    elif cv == '2':
        obj=Product.objects.filter(cat=2)
        context={'product':obj}
        return render(request,'index.html',context)
    elif cv == '3':
        obj=Product.objects.filter(cat=3)
        context={'product':obj}
        return render(request,'index.html',context)
    else:
        obj=Product.objects.filter(cat=5)
        context={'product':obj}
        return render(request,'index.html',context)



def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        p=Product.objects.filter(id=pid)
        obj=Cart.objects.create(uid=u[0],pid=p[0],cprice=p[0].price)
        obj.save()
        return redirect('/')
    else:
        return redirect('login')
    
   
def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    total_product =c.count()
    s=0
    cnt=0
    for i in c:
        cnt+=(i.qty)
        s +=float(i.pid.price * i.qty)    
    context={'product':c,'total':s,"total_product":total_product,"cnt":cnt}
    return render(request,'cart.html',context)
    


def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')



def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        qty=c[0].qty + 1 
        c.update(qty=qty)
        return redirect("/cart")
    elif c[0].qty>1:
        qty=c[0].qty - 1 
        c.update(qty=qty,cprice=c[0].pid.price*qty)
        return redirect("/cart")
    else:
        return redirect("/cart")
    


def range(request):
    if request.method == "GET":
        min=request.GET["min"]
        max=request.GET["max"]
    # select pname from products where price>=min and price<=max
        c1=Q(price__gte=min)
        c2=Q(price__lte=max)
        obj=Product.objects.filter(c1 & c2)
        context={'product':obj}
        return render(request,'index.html',context)
    


def aboutus(request):
    return render(request, 'about.html')

def contact(request):
    return render(request,'contact.html')




def sort(request, order='low_to_high'):
    products = Product.objects.filter(is_active=True)

    if order == 'low_to_high':
        products = products.order_by('price')
    elif order == 'high_to_low':
        products = products.order_by('-price')
    else:
        products = products.order_by('price')

    context = {'product': products, 'order': order}
    return render(request, 'index.html', context)



def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        obj=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        obj.save()
        x.delete()
    return redirect('/makepayment')


import razorpay
def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_Wwpuedf0lsd9BT", "ziqHn0zH8haHcja07Q2aRYwe"))

    data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    data={"payment":payment}
    return render(request,"pay.html")


