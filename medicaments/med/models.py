from django.db import models


# Create your models here.
class Administrateur(models.Model):
    username= models.CharField(max_length=50, unique=False)
    email = models.CharField(max_length=50, unique=True)
    password= models.CharField(max_length=50)
    avatar = models.ImageField(null=False, blank=False, upload_to='images/')  # Ajout d'un champ pour l'avatar


class CategoryMedecine(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description= models.CharField(max_length=500)
    
class Medecine(models.Model):
    medecine_name= models.CharField(max_length=70, unique=True)
    price=models.CharField(max_length=6)
    quantity=models.IntegerField()
    expire_date= models.DateField()
    description= models.CharField(max_length=500)
    delevery_date= models.DateField()
    avatar = models.ImageField(null=False, blank=False, upload_to='images/')  # Ajout d'un champ pour l'avatar
    category= models.ForeignKey(CategoryMedecine, on_delete=models.CASCADE, default=1)

class Employee(models.Model):
    emp_name= models.CharField(max_length=100)
    description= models.CharField(max_length=500)
    poste= models.CharField( max_length=50)
    email= models.EmailField( max_length=54)
    employee_id= models.CharField( max_length=50)
    avatar = models.ImageField(null=False, blank=False, upload_to='images/')  # Ajout d'un champ pour l'avatar

class Provider(models.Model):
    name= models.CharField( max_length=50)
    entreprise= models.CharField( max_length=50)
    avatar = models.ImageField(null=False, blank=False, upload_to='images/')  # Ajout d'un champ pour l'avatar

    
class Buys(models.Model):
    product= models.ForeignKey(Medecine, on_delete=models.CASCADE)
    date= models.DateField( auto_now_add=True)
    provider=models.ForeignKey(Provider, on_delete= models.CASCADE)
    quantity=models.IntegerField()
    avatar = models.ImageField(null=False, blank=False, upload_to='images/')  # Ajout d'un champ pour l'avatar

class Sales(models.Model):
    client_Name= models.CharField( max_length=50)
    product= models.ForeignKey(Medecine, on_delete=models.CASCADE)
    date = models.DateField( auto_now_add=True)
    quantity= models.CharField( max_length=50)
    Admin= models.ForeignKey(Administrateur, on_delete=models.CASCADE)

