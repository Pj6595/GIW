# Jaime Antolín, Álvar Domingo, Pablo Jurado y Leire Osés declaramos que esta solución es fruto exclusivamente
# de nuestro trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos
# obtenido la solución de fuentes externas, y tampoco hemos compartido nuestra solución
# con nadie. Declaramos además que no hemos realizado de manera deshonesta ninguna otra
# actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from mongoengine import *
from mongoengine.connection import connect
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.errors import ValidationError
from mongoengine.fields import ComplexDateTimeField, EmbeddedDocumentField, FloatField, IntField, ListField, ReferenceField, StringField
import string
import math

connect('giw_mongoengine')

def checkString(stri):
    if not isinstance(stri, str):
        raise ValidationError("El valor del StringField no es un string")

def checkInt(inte):
    if not isinstance(inte, int):
        raise ValidationError("El valor del IntField no es un int")

def checkFloat(floater):
    if not isinstance(floater, float):
        raise ValidationError("El valor del FloatField no es un float")

def checkList(lista):
    if not isinstance(lista, list):
        raise ValidationError("El valor del ListField no es una lista")

class Tarjeta(EmbeddedDocument):
    nombre = StringField(required=True, min_length = 2)
    numero = StringField(required=True, min_length=16, max_length=16,  regex = "[0-9]")
    mes = StringField(required = True, min_length=2, max_length=2,  regex = "[0-9]")
    año = StringField(required = True, min_length=2, max_length=2,  regex = "[0-9]")
    ccv = StringField(required=True, min_length=3, max_length=3,  regex = "[0-9]")

    def clean(self):
        checkString(self.numero)
        checkString(self.ccv)
        if not self.ccv.isnumeric():
            raise ValidationError("El ccv no tiene un formato numérico correcto")

        checkString(self.mes)
        if not self.mes.isnumeric():
            raise ValidationError("El mes no tiene un formato numérico correcto")
        mesNum = int(self.mes)
        if(mesNum < 1 or mesNum >12): 
            raise ValidationError("Mes no valido")
        if not self.numero.isnumeric():
            raise ValidationError("El numero de tarjeta contiene cosas que no son números")

class Producto(Document):
    codigo_barras = StringField(min_length=13, max_length=13, regex="[0-9]", primary_key=True)
    nombre = StringField(required=True, min_length=2)
    categoria_principal = IntField(required=True)
    categorias_secundarias = ListField(IntField(), required=False)
    
    def clean(self):
        checkList(self.categorias_secundarias)
        checkString(self.codigo_barras)
        checkInt(self.categoria_principal)
        suma = 0
        for i in range(12):
            peso = 0
            digito = int(self.codigo_barras[i])
            if i%2 == 0:
                peso= 1
            else:
                peso = 3
            suma += digito * peso
        
        proximoMultiplo = (math.trunc(suma/10) + 1) *10
        if int(self.codigo_barras[12]) != (proximoMultiplo - suma):
            raise ValidationError("El dígito de control del código de barras no es correcto")

        if len(self.categorias_secundarias) > 0 and self.categorias_secundarias[0] != self.categoria_principal:
            raise ValidationError("La lista de categorías secundarias no comienza con la categoría principal")

        

class Linea(EmbeddedDocument):
    num_items = IntField(required = True, min_value=0)
    precio_item = FloatField(required = True, min_value=0)
    name = StringField(required=True, min_length = 2)
    total = FloatField(required = True, min_value=0)
    ref =  ReferenceField(Producto, required = True)

    def clean(self):
        checkString(self.name)
        if not isinstance(self.ref, Producto):
            raise ValidationError("La referencia a un producto no es correcta")
        checkString(self.ref.nombre)
        checkInt(self.num_items)
        checkFloat(self.precio_item)
        checkFloat(self.total)
        if self.name != self.ref.nombre:
            raise ValidationError("El nombre de el producto referenciado no se corresponde con el de la línea")
        if self.total != self.num_items*self.precio_item:
            raise ValidationError("El precio total de la línea no se corresponde con el precio individual por número de items")

class Pedido(Document):
    total = FloatField(required = True, min_value=0)
    fecha = ComplexDateTimeField(required=True)
    lineas = ListField(EmbeddedDocumentField(Linea), required=True)

    def clean(self):
        checkFloat(self.total)
        checkList(self.lineas)
        sumaPrecio = 0
        productosReferenciados = {}
        for i in self.lineas:
            sumaPrecio += i.total
            if i.ref not in productosReferenciados.keys():
                productosReferenciados[i.ref] = True
            else:
                raise ValidationError("Hay más de una línea que referencia un mismo producto")
        if sumaPrecio != self.total:
            raise ValidationError("El precio total no se corresponde a la suma de los precios de cada item")

        checkList(self.lineas)

class Usuario(Document):
    dni =  StringField(primary_key=True, max_length=9, min_length=9, regex = "[0-9]+[A-Z]")
    nombre = StringField(required=True, min_length = 2)
    apellido1 = StringField(required=True, min_length = 2)
    apellido2 = StringField()
    f_nac = StringField(required=True, min_length= 10, max_length=10, regex="")
    tarjetas = ListField(EmbeddedDocumentField(Tarjeta))
    pedidos = ListField(ReferenceField(Pedido, reverse_delete_rule=4))

    def clean(self):
        checkString(self.dni)
        checkString(self.f_nac)

        if len(self.dni) != 9:
            raise ValidationError("La longitud del DNI no es correcta")

        if len(self.f_nac) != 10:
            raise ValidationError("La longitud de la fecha de nacimiento no es correcta")

        listaLetras = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E']
        letra = self.dni[8]
        if letra not in string.ascii_uppercase:
            raise ValidationError("La letra del DNI no se ha encontrado o tiene un formato incorrecto")
        numero = int(self.dni[0:8])
        if letra != listaLetras[numero%23]:
            raise ValidationError("La letra del DNI es incorrecta")

        fnac1 = self.f_nac[0:4]
        fnac2 = self.f_nac[5:7]
        fnac3 = self.f_nac[8:10]
        if self.f_nac[4] != "-" or self.f_nac[7]!="-" or not fnac1.isnumeric() or not fnac2.isnumeric() or not fnac3.isnumeric() or not int(fnac2) < 13 or not int(fnac3) < 31:
            raise ValidationError("El formato de la fecha de nacimiento es incorrecto")

def inserta():
    tarjeta1 = Tarjeta(nombre ="Joselito Manzanas", numero="5383914025409234",mes= "03", año="23", ccv="594")
    tarjeta2 = Tarjeta(nombre="Joselito Manzanas", numero="5383984025609334", mes="12", año="26",ccv="666")
    tarjeta3 = Tarjeta(nombre ="Miguelon Martinez Puerta", numero="5383914025409234", mes="04", año="24", ccv="549")
    tarjeta4 = Tarjeta(nombre ="Miguelon Martinez Puerta", numero="6374919875409265", mes="06", año="22", ccv="658")

    producto1 = Producto(codigo_barras="1886318417087", nombre="Toallas", categoria_principal=2, categorias_secundarias=[2,4,5,6])
    producto2 = Producto(codigo_barras="4561405092114", nombre="Sillas", categoria_principal=1, categorias_secundarias=[1,11,12])
    producto3 = Producto(codigo_barras= "6258597106542",nombre="Sal", categoria_principal=3, categorias_secundarias=[3,4,5,6])
    producto4 = Producto(codigo_barras="6542505391084", nombre="Pimienta", categoria_principal=4, categorias_secundarias=[4,11,12])

    producto1.save()
    producto2.save()
    producto3.save()
    producto4.save()

    pedido1 = Pedido(total =55, fecha ="2017,10,22,10,15,24,000000", lineas =[Linea(num_items =3,precio_item = 5, name = "Toallas", total = 15, ref =producto1), Linea(num_items =2, precio_item =20, name = "Sillas", total = 40, ref =producto2)])
    pedido2 = Pedido(total =510, fecha = "2018,11,12,11,12,22,000000", lineas =[Linea(num_items =5, precio_item =100, name = "Sal", total = 500, ref =producto3), Linea(num_items =10, precio_item =1, name = "Pimienta", total = 10, ref =producto4)])
    pedido3 = Pedido(total =1550, fecha = "2019,11,12,11,12,22,000000", lineas =[Linea(num_items =10, precio_item =5, name = "Toallas", total = 50, ref =producto1), Linea(num_items =15, precio_item =100, name = "Sal", total = 1500, ref =producto3)])
    pedido4 = Pedido(total =200, fecha ="2020,11,12,11,12,22,000000", lineas =[Linea(num_items =5, precio_item =20, name = "Sillas", total = 100, ref =producto2), Linea(num_items =100, precio_item =1, name = "Pimienta", total = 100, ref =producto4)])

    pedido1.save()
    pedido2.save()
    pedido3.save()
    pedido4.save()

    usuario1 = Usuario(dni="22246432G", nombre= "Joselito", apellido1="Manzanas", apellido2="Platanero", f_nac="1984-12-20", tarjetas=[tarjeta1, tarjeta2] , pedidos=[pedido1, pedido2])
    usuario2 = Usuario(dni= "90662513D", nombre= "Miguelon",apellido1="Martinez", apellido2="Puerta", f_nac="2000-02-02", tarjetas=[tarjeta3, tarjeta4] , pedidos=[pedido3, pedido4])

    usuario1.save()
    usuario2.save()

inserta()