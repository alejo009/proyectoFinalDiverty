from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.

 
class Promociones(models.Model):
    id_promocion=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=254)
    precio=models.IntegerField(null=False,blank=False)
    fecha=models.DateField(null=False,blank=False,max_length=254)

    def __str__(self):
        return str(self.id_promocion)
   
class Atracciones (models.Model):
    id_atraccion=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=254,blank=False,null=False,unique=True)
    capacidad=models.SmallIntegerField(blank=False,null=False)
    fecha=models.DateField(null=False,blank=False,max_length=254)
    precio=models.IntegerField(null=False,blank=False)
    def __str__(self) :
        return str(self.nombre)
   
class Clientes(models.Model):
    id_cliente=models.AutoField(primary_key=True)
    identificacion = models.IntegerField(unique=True, null=False, blank=False)
    nombre=models.CharField(max_length=254,blank=False,null=False)
    apellido=models.CharField(max_length=254,blank=False,null=False)
    edad=models.IntegerField(null=False,blank=False)
    direccion=models.CharField(max_length=150,blank=False )
    telefono=models.CharField(max_length=15,blank=False,null=False)
    def __str__(self):
        return  str(self.nombre)
def validate_image(fieldfile_obj):

    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

class Boletas_producto(models.Model):
    codigo_producto=models.CharField(max_length=20,unique=True)
    nombre_boleta_producto=models.CharField(max_length=100)
    foto=models.ImageField(upload_to="productos",validators=[validate_image])
    precio=models.IntegerField()
    stock=models.IntegerField()
    descuento=models.ForeignKey(Promociones,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return f"{self.nombre_boleta_producto}"
class Ventas(models.Model):
    id_venta=models.AutoField(primary_key=True)
    fecha=models.DateField(null=False,blank=False,max_length=254)
    costo=models.IntegerField(null= False,blank=False)
    clientes=models.ForeignKey(Clientes,on_delete=models.DO_NOTHING)
    boletas=models.ForeignKey(Boletas_producto,on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.id_venta)

class Reservas(models.Model):
    id_reserva=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=254,blank=False,null=False)
    fecha=models.DateField(null=False,blank=False)
    atracciones_reservas=models.ForeignKey(Atracciones,on_delete=models.DO_NOTHING,related_name="%(class)s_atracciones")
    def __str__(self) :
        return str(self.nombre)


class Empleados(models.Model):
    id_empleado=models.AutoField(primary_key=True)
    identificacion = models.IntegerField(unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=100,null=False,blank=False)
    apellido = models.CharField(max_length=100,null=False,blank=False)
    correo = models.EmailField(max_length=200,unique=True)
    def __str__(self) :
        return str(self.nombre)


class Usuario(models.Model):
    ROL = (
        (1,'Administrador'),
        (2,'Empleado'),
        (3,'Cliente'),
    )
    usuario=models.CharField(max_length=100, unique=True,default="")
    correo = models.EmailField(max_length=200,null=False,blank=False,unique=True)
    clave = models.CharField(max_length=254,blank=False,null=False)
    rol=models.IntegerField(choices=ROL,default=3)
    def __str__(self) :
        return str(self.usuario)


class Aviso(models.Model):
    id_aviso=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=254)
    imagen=models.ImageField(upload_to="Aviso",validators=[validate_image])

class Pedido(models.Model):


    cliente=models.ForeignKey(Usuario,on_delete=models.DO_NOTHING)
    fecha=models.DateTimeField("Fecha y hora del pedido")
    direccion_de_envio=models.CharField(max_length=254)
    ESTADO=(
        ('1','Nuevo'),
        ('2','Confirmado'),
        ('3','Enviado'),
        ('4','Cancelado'),
    )
    estado=models.CharField(max_length=1,choices=ESTADO,default='1')
    def __str__(self):
        return f"Pedido: {self.id} - Cliente: {self.cliente}"
class PedidoProducto(models.Model):
    pedido=models.ForeignKey(Pedido,on_delete=models.DO_NOTHING)
    producto=models.ForeignKey(Boletas_producto,on_delete=models.DO_NOTHING)
    cantidad=models.IntegerField()
    precio=models.IntegerField()
    def __str__(self):
        return f"Pedido: {self.pedido} - Producto: {self.producto}"
