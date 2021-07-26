
from django.core.exceptions import ValidationError
from django.core import validators
from django import forms
from django.db import models
from django.db.models.fields import IntegerField
from django.forms import fields, widgets
from datetime import date
from .models import Clientes,Empleados,Ventas,Promociones,Atracciones,Reservas,Aviso,Boletas_producto,Pedido,PedidoProducto




class ClienteForm(forms.ModelForm):
    identificacion=forms.IntegerField(required=True,validators=[validators.validate_integer])
    nombre=forms.CharField(required=True,max_length=50,validators=[validators.validate_slug])
    apellido=forms.CharField(required=True,max_length=50)
    edad=forms.IntegerField(required=True,min_value=1,max_value=120,validators=[validators.validate_integer])
    direccion=forms.CharField(required=True,min_length=18,max_length=50)
    telefono=forms.CharField(required=True,min_length=11,max_length=20,validators=[validators.validate_slug])

    class Meta:
        model=Clientes
        fields= ('identificacion','nombre','apellido','edad','direccion','telefono')
    
    def clean_identificacion(self):
        identificacion=self.cleaned_data["identificacion"]
        conversion=str(identificacion)
        if len(conversion)>10:
            raise forms.ValidationError("La cedula debe contener 10 digitos")
        return conversion
    def clean_nombre(self):
        nombre=self.cleaned_data["nombre"]
        if any(char.isdigit() for char in nombre):
            raise forms.ValidationError("El nombre no puede contener dígitos.")
        return nombre

    def clean_apellido(self):
        apellido=self.cleaned_data["apellido"]
        if any(char.isdigit() for char in apellido):
            raise forms.ValidationError("El apellido no puede contener digitos")
        return apellido
    def clean_nombre(self):
        nombre=self.cleaned_data["nombre"]
        if (len(nombre)<3 or len(nombre)>14):
            raise forms.ValidationError("Ingrese un nombre en 3 y 14 caracteres")
        return nombre


class EmpleadoForm(ClienteForm):
    edad=None
    direccion=None
    telefono=None
    class Meta:
        model=Empleados
        fields='__all__'

class VentasForm(ClienteForm):
    costo=forms.IntegerField(required=True,min_value=10000,max_value=800000)
    identificacion=None
    nombre=None
    apellido=None
    edad=None
    direccion=None
    telefono=None
    class Meta:
        model=Ventas
        fields=['fecha','costo','clientes','boletas']

    def clean_fecha(self):
        today=date.today()
        fecha= self.cleaned_data['fecha']
        if fecha>(today):
            raise forms.ValidationError("La fecha no puede ser mayor al dia de hoy")
        return fecha
   
class PromocionesForm(VentasForm):
    costo=None
    precio=forms.IntegerField(required=True,min_value=10000,max_value=800000)
    class Meta:
        model=Promociones
        fields=['nombre','precio','fecha']
   
        

class AtraccionesForm(VentasForm):
    capacidad=forms.IntegerField(required=True,min_value=1,max_value=150)
    precio=forms.IntegerField(required=True,min_value=10000,max_value=800000)
    costo=None
    class Meta:
        model=Atracciones
        fields='__all__'

class ReservasForm(VentasForm):
    costo=None
    
    class Meta:
        model=Reservas
        fields='nombre','fecha','atracciones_reservas'


class AvisoForm(ReservasForm):

    class Meta:
        model=Aviso
        fields='nombre','imagen'

class Boletas_productoForm(forms.ModelForm):
    codigo_producto=forms.CharField(required=True,min_length=10)
    precio=forms.IntegerField(required=True,min_value=10000,max_value=800000)
    class Meta:
        model=Boletas_producto
        fields='codigo_producto','nombre_boleta_producto','foto','precio','stock','descuento'
    def clean_nombre_boleta_producto(self):
        nombre_boleta_producto=self.cleaned_data["nombre_boleta_producto"]
        if any(char.isdigit() for char in nombre_boleta_producto):
            raise forms.ValidationError("El nombre no puede contener dígitos.")
        return nombre_boleta_producto
 

class PedidoProductoForm(forms.ModelForm):
    cantidad=forms.IntegerField(min_value=1,max_value=250)
    class Meta:
        model=PedidoProducto
        fields=['pedido','producto','cantidad','precio']

class PedidoForm(PedidoProductoForm):
    cantidad=None
    class Meta:
        model=Pedido
        fields=['cliente','fecha','direccion_de_envio','estado']



