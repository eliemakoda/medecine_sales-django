from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Administrateur, CategoryMedecine,Medecine,Sales, Buys, Employee, Provider
from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Sum,F
from django.db.models.functions import TruncDate, TruncDay, TruncWeek
# Create your views here.
import os 
# from .models import Medecine
from django.utils import timezone
# from datetime import timedelta
from django.db.models.functions import TruncMonth
from datetime import date, datetime, timedelta
import math
from django.db import models
def calculate_total_sales():
        total_sales = Sales.objects.all().annotate(
            total=Sum(F('product__price') * F('quantity'), output_field=models.FloatField())
        ).values('total').first()
        return total_sales['total'] if total_sales else 0
    
def calculate_total_Buy():
        total_sales = Buys.objects.all().annotate(
            total=Sum(F('product__price') * F('quantity'), output_field=models.FloatField())
        ).values('total').first()
        return total_sales['total'] if total_sales else 0
    
    
def Index(request):
    CriticalStock= Medecine.objects.filter(quantity__lte=10) #every product that's quantity is less or equal 10
    today= date.today()
    expiry_date_threshold = today + timedelta(days=10) # every product that'll expire in less than 10 days
    expire_soon_med= Medecine.objects.filter(expire_date__lte=expiry_date_threshold)
    medlist=[]
    for med in expire_soon_med:
        if med.expire_date<today:
            tmp={
                "pk":med.pk,
                "medecine_name":med.medecine_name,
                "price":med.price,
                "quantity":med.quantity,
                "expire_date":med.expire_date,
                "description":med.description,
                "delevery_date":med.delevery_date,
                "avatar":med.avatar,
                "category":med.category,
                "status":True
            }
            medlist.append(tmp)
        else:
            tmp={
                "pk":med.pk,
                "medecine_name":med.medecine_name,
                "price":med.price,
                "quantity":med.quantity,
                "expire_date":med.expire_date,
                "description":med.description,
                "delevery_date":med.delevery_date,
                "avatar":med.avatar,
                "category":med.category,
                "status":False
            }
            medlist.append(tmp)           
        
    top_selling_products = Sales.objects.values('product__medecine_name').annotate(total_sales=Count('product__medecine_name')).order_by('-total_sales')[:3]
    top_selling_product = Sales.objects.values('product__medecine_name').annotate(total_sales=Count('product__medecine_name')).order_by('-total_sales').first()
   
    sales_data = Sales.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_sales=Sum('product__price'))
    labels = [data['month'].strftime('%B %Y') for data in sales_data]
    values = [data['total_sales'] for data in sales_data]
    allSalesAmount= int(calculate_total_sales())
    allBuysAmount= int(calculate_total_Buy())
    total_expense= allSalesAmount+ allBuysAmount
    
    sales_data = Sales.objects.values('date').annotate(total_sales=Sum('product__price')).order_by('date')
    
    labels = [data['date'].strftime('%Y-%m-%d') for data in sales_data]
    values = [data['total_sales'] for data in sales_data]
    #  request.session['username'] = user.username
    #         request.session['email'] = user.email
    #         request.session['password'] = user.password
    #         request.session['avatar'] = user.avatar.url
    buyes = Buys.objects.all().order_by('date')
    dates = [buy.date for buy in buyes]
    quantities = [buy.quantity for buy in buyes]
    
    
    sales_data = Sales.objects.all().values('date').annotate(total_quantity=Sum('quantity')).order_by('date')
    datess = [data['date'] for data in sales_data]
    quantitiess = [data['total_quantity'] for data in sales_data]
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    today = timezone.now().date()
    ten_days_from_now = today + timedelta(days=10)

    expiring_medecines = Medecine.objects.filter(expire_date__lte=ten_days_from_now)

    medecine_names = [medecine.medecine_name for medecine in expiring_medecines]
    expire_dates = [medecine.expire_date.strftime('%Y-%m-%d') for medecine in expiring_medecines]

    liste= []
    for i in range(len(datess)):
        liste.append({"y":quantitiess[i], "label":datess[i]})
    return render(request, "index.html", context={  'medecine_names': medecine_names,
        'expire_dates': expire_dates,"datess":datess, "quantitiess":quantitiess, "log":userDetails,  'dates': dates,
        'quantities': quantities,"log":userDetails,"totExp":total_expense,"allbuy":allBuysAmount,"allsales":allSalesAmount,"labels":labels,"values":values,"meds":CriticalStock, 
        "expmeds":medlist, "topsales": top_selling_products, "top":top_selling_product,
        "datapoints":liste
        })


def addBuy(request):
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    pv= Provider.objects.all()
    product= Medecine.objects.all()
    if request.method=="POST":
        prod= Medecine.objects.get(pk=request.POST.get("medecine"))
        prov= Provider.objects.get(pk=request.POST.get('provider'))
        quantity= int(float(request.POST.get("quantity")))
        avatar = request.FILES.get('userAvatar')  
        img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
        with open(img_path, 'wb') as img_file:
                for chunk in avatar.chunks():
                    img_file.write(chunk)
        buy= Buys(product=prod, provider= prov,quantity=quantity,  avatar=avatar)
        prod.quantity=int(float(prod.quantity))+quantity
        prod.save()
        buy.save()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request, "addbuy.html" , context={"log":userDetails,"medecine":product, "provider":pv})

def addCategory(request):
    if request.method == "POST":
        category_name= request.POST.get("projectname")
        catDescription= request.POST.get("projectdesc")
        category = CategoryMedecine(category_name=category_name, description=catDescription)
        category.save()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request, 'addCategory.html', context={"log":userDetails})

def addEmployee(request):
    if request.method=="POST":
        name= request.POST.get('name')
        desc= request.POST.get("empDesc")
        occ= request.POST.get("Occupation")
        email= request.POST.get("email")
        IdEmploye= request.POST.get('id')
        avatar = request.FILES.get('userAvatar')  
        img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
        with open(img_path, 'wb') as img_file:
                for chunk in avatar.chunks():
                    img_file.write(chunk)
        emp= Employee(emp_name=name,description=desc, poste=occ,email=email,employee_id=IdEmploye,avatar=avatar)
        emp.save()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    return render(request, "addemployee.html", context={"log":userDetails})

def addMedecine(request):
        userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

        if request.method== "POST":
            name= request.POST.get("projectname")
            description= request.POST.get("projectdesc")
            dateStart= request.POST.get("start")
            dateEnd =request.POST.get("end")
            prix= request.POST.get("cost")
            categoryID= request.POST.get("category")
            avatar = request.FILES.get('userAvatar')  
            img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
            with open(img_path, 'wb') as img_file:
                for chunk in avatar.chunks():
                    img_file.write(chunk)
            quantity= request.POST.get("quantity")
            userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

            try:
                cat = CategoryMedecine.objects.get(pk=categoryID)
                Medecines= Medecine(medecine_name=name,price=prix, quantity=quantity,expire_date=dateEnd,description=description,delevery_date=dateStart, avatar=avatar,category=cat )
                Medecines.save()
            except CategoryMedecine.DoesNotExist:
                category= CategoryMedecine.objects.all()
                return render(request, "addMedcine.html", context={"category":category, "log":userDetails})
        category= CategoryMedecine.objects.all()
        return render(request, "addMedcine.html", context={"category":category, "log":userDetails})

def addsales(request):
    auth= True
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    prod= Medecine.objects.all()
    if not request.session.get('id'):
        auth=False
    if request.method=="POST":
        client= request.POST.get("clientname")
        product= Medecine.objects.get(pk=request.POST.get("product"))
        date= request.POST.get("start")
        quantity= request.POST.get("quantity")
        userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

        if auth==True:
            adminId=request.session.get('id')
        else:
            adminId=2
        Admin=Administrateur.objects.get(pk=adminId)
        product.quantity=int(float(product.quantity))-int(float(quantity)) #retrait du stock
        if int(product.quantity<0):
            product.quantity=0
        if int(product.quantity)<int(quantity):
            return render(request, "addsales.html", context={"log":userDetails, "product":prod, "error":"stock aren't suffisant for this operation! please fill the stock first!..."})
        newSales= Sales(client_Name=client,product=product, date=date,quantity=quantity,Admin=Admin)
        product.save()
        newSales.save()
    return render(request, "addsales.html", context={"log":userDetails,"product":prod})

def addSuplier(request):
    category= CategoryMedecine.objects.all()
    if request.method== "POST":
        name= request.POST.get("Suppliername")
        clinic= request.POST.get("Clinicname")
        avatar = request.FILES.get('userAvatar')  
        img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
        with open(img_path, 'wb') as img_file:
            for chunk in avatar.chunks():
                img_file.write(chunk)  
        pv = Provider(name=name,entreprise=clinic,avatar=avatar)
        pv.save()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request, 'addSupplier.html', context={"log":userDetails,"category": category})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('Password')
        try:
            user= Administrateur.objects.get(email=email, password= password)
            request.session['username'] = user.username
            request.session['email'] = user.email
            request.session['password'] = user.password
            request.session['avatar'] = user.avatar.url
            request.session['id'] = user.pk

            return redirect("accueil")
        except Administrateur.DoesNotExist:
            messages.error(request, 'Email ou mot de passe incorrect')
            redirect("accueil")

    return render(request, "auth-login.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpassword')
        useremail= request.POST.get("useremail")
        avatar = request.FILES.get('userAvatar')  
        img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
        with open(img_path, 'wb') as img_file:
            for chunk in avatar.chunks():
                img_file.write(chunk)
        admin= Administrateur(username= username, email= useremail, password=password, avatar=avatar)
        admin.save()
        return render(request, "auth-login.html")
    return render(request, "auth-register.html")

def billdetail(request,id):
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request,"billdetails.html", context={
        "log":userDetails
    })

def billist(request):
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    ventes=Sales.objects.values('date', 'client_Name', 'product', 'quantity', 'Admin').annotate(total=Count('id'))
    return render(request, "billlist.html" ,context={"log":userDetails,"ventes": ventes})

def buylist(request):
    # = Buys.objects.all()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    buy=Buys.objects.values('date', 'avatar', 'product__medecine_name', 'quantity', 'provider__name').annotate(total=Count('id'))

    return render(request, 'buyList.html', context={"log":userDetails,"buys":buy})

def categorylist(request):
    cat = CategoryMedecine.objects.all()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request , "categorylist.html", context={"log":userDetails,"cats":cat})

def employeelist(request):
    emp= Employee.objects.all()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request, 'employeelist.html',context={"log":userDetails,"employees":emp})

def listsuplier(request):
    supList= Provider.objects.all()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    return render(request, 'listSupplier.html', context={"log":userDetails,"provider":supList})

def medecinedetail(request, id):
    med= Medecine.objects.get(pk=id)
    lastMed= Medecine.objects.order_by('-pk')[:3]
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request, "medecinedetail.html", context={"log":userDetails,"target":med, "lastMed":lastMed})

def medecinelist(request):
    cat= CategoryMedecine.objects.all()
    med= Medecine.objects.all()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request, "medecinelist.html", context={"log":userDetails,"medecine":med,"category":cat})

def saleslist(request):
    data= Sales.objects.all()
    # print(data)
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    return render(request, "saleslist.html", context={"log": userDetails,"sales":data})

def updateemployee(request,id):
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    return render(request, "updateemployee.html", context={"log": userDetails})

def updateSuplier(request, id):
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    return render(request, "updateSupplier.html", context={"log":userDetails})

def addadmin(request):
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    return render(request, "addAdmin.html", context={"log":userDetails})
class achatMed:
    def __init__(self,medecine_name ,quantity,price,total_price, client):
        self.name= medecine_name
        self.quantity= quantity 
        self.price= price
        self.total= total_price
        self.client= client
        
def NewBill(request, clientName, date):
    sales_data= Sales.objects.filter(client_Name=clientName, date=date)
    med=[]
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    priceHT=0
    for sale in sales_data:
        medecine_name = sale.product.medecine_name
        quantity = sale.quantity
        price = sale.product.price
        client= sale.client_Name
        total_price = int(sale.quantity) * int(sale.product.price)
        med.append({"pk":sale.pk,"name":medecine_name,"quantity":quantity,"price":price, "client":client,"total":total_price})
        # # achatMed(medecine_name,quantity,price,total_price, client)
        # # med.append()
        # print(med)
        priceHT+= total_price
        ttc= (priceHT*19.25)/100
        ttc+= priceHT
        ttc= int(ttc)
    actualDate= datetime.now()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }

    fakeNumber= "ORDER ID: "+"CBM"+"-"+ str(actualDate.hour)+"-"+ str(actualDate.second)+ "-"+str(actualDate.year)[2:]
    return render(request, "Sales.html", context={"log":userDetails,"meds":med, "total":priceHT, "ttc":ttc, "clientName":clientName, "date":date,"fakeNumber":fakeNumber})

        
def ProviderBill(request, clientName, date):
    pv= Provider.objects.get(name=clientName)
    sales_data= Buys.objects.filter(provider=pv, date=date)
    med=[]
    priceHT=0
    ttc=0
    for elt in sales_data:
        name= elt.product.medecine_name
        totalPrice= int(elt.product.price)* int( elt.quantity)
        priceHT+=totalPrice
        med.append({"name":name, "total":totalPrice, "pk":elt.pk})
    ttc= (priceHT*19.25)/100
    ttc+= priceHT
    ttc= int(ttc) 
    tva= (priceHT*19.25)/100
    actualDate= datetime.now()
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    fakeNumber= "ORDER ID: "+"CBM"+"-"+ str(actualDate.hour)+"-"+ str(actualDate.second)+ "-"+str(actualDate.year)[2:]
    return render(request, "providerBill.html", context={"log":userDetails,"tva":int(tva),"meds":med, "total":priceHT, "ttc":ttc, "provider":pv, "date":date,"fakeNumber":fakeNumber})

    
def ListMedCatg(request,id):
    userDetails={"username":request.session.get('username'),"pk":request.session.get("id"), "email": request.session.get('email'), "avatar": request.session.get("avatar") , "password": request.session.get("password") }
    cat= CategoryMedecine.objects.all()
    target= CategoryMedecine.objects.get(pk=id)
    med= Medecine.objects.filter(category=target)
    return render(request, "ListMedCatg.html", context={"log":userDetails,"medecine":med,"category":cat})

def logout(request):
    del request.session['username']
    del request.session['email'] 
    del request.session['password'] 
    del request.session['avatar'] 
    del request.session['id']
    return redirect("authLogin")