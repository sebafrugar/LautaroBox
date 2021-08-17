from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    
            errors['email'] = "El mail no es valido!"
        if len(postData['first_name']) < 3:
            errors["first_name"] = "Nombre debe tener al menos 3 caracteres"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Apellido debe tener al menos 3 caracteres"
        if postData['password'] != postData['password_conf']:
            errors['password_match'] = "Passwords no coincide"
        if len(postData['password']) < 8:
            errors['len_password'] = "Minimo 8 caracteres"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=500)
    birth_date = models.DateTimeField()
    objects = UserManager()
    def __str__(self):
        return f"<{self.first_name} {self.last_name} {self.email} {self.id}>"

class infoclase(models.Model):
    nombre_clase = models.CharField(max_length=50)

class diaclase(models.Model):
    dia_clase = models.DateField()
    hora_comienzo = models.TimeField()
    hora_termino = models.TimeField()
    lista_estudiante = models.ManyToManyField(User)
    info = models.ForeignKey(infoclase, on_delete=models.CASCADE, null=True)

class Shop(models.Model):
    mensualidad = models.CharField(max_length=100)
    items = models.CharField(max_length=100, null=True)
    pagado = models.ForeignKey(User,on_delete=models.CASCADE)





