from django.contrib import admin
from django.urls import path
from med import views
from datetime import date
# addAdmin
urlpatterns = [
    path("",views.login,name="authLogin"),
    path("accueil", views.Index, name="accueil"),
    path("addbuy", views.addBuy, name="addbuy"),
    path("addAdmin", views.addadmin, name="addAdmin"),
    path("addcategory",views.addCategory,name="addcategory"),
    path("addemployee",views.addEmployee,name="addemployee"),
    path("addMedecine",views.addMedecine,name="addMedecine"),
    path("addsales",views.addsales,name="addsales"),
    path("addsupplier",views.addSuplier,name="addsupplier"),
    path("authRegister",views.register,name="authRegister"),
    path("billdetails/<int:id>",views.billdetail,name="billdetails"),
    path("billist",views.billist,name="billist"),
    path("buylist",views.buylist,name="buylist"),
    path("categoryList",views.categorylist,name="categoryList"),
    path("employeelist",views.employeelist,name="employeelist"),
    path("listSupplier",views.listsuplier,name="listSupplier"),
    path("medecinedetails/<int:id>",views.medecinedetail,name="medecinedetails"),
    path("medecinelist",views.medecinelist,name="medecinelist"),
    path("saleslist",views.saleslist,name="saleslist"),
    path("updateemployee/<int:id>",views.updateemployee,name="updateemployee"),
    path("updateSupplier/<int:id>",views.updateSuplier,name="updateemployee"),
    path("salesbill/<str:clientName>/<str:date>/",views.NewBill,name="salesbill"),
    path("buysbill/<str:clientName>/<str:date>/",views.ProviderBill,name="buysbill"),
    path("medCategory/<int:id>",views.ListMedCatg,name="medCategory"),
    path("logout",views.logout,name="logout"),

]

