from django.contrib import admin

from .models import  Promociones,Atracciones,Clientes,Ventas,Reservas,Empleados,Usuario,Aviso,Boletas_producto,Pedido,PedidoProducto

class promocionesAdmin(admin.ModelAdmin):
    list_display = ('id_promocion','nombre','precio','fecha')
    search_fields = ['id_promocion']
    
admin.site.register(Promociones,promocionesAdmin)

class AtraccionesAdmin(admin.ModelAdmin):
    list_display=('id_atraccion','nombre','capacidad','fecha','precio')
    list_filter=['nombre']
    search_fields=['id_atraccion','nombre']
admin.site.register(Atracciones,AtraccionesAdmin)

class ClientesAdmin(admin.ModelAdmin):
    list_display=('id_cliente','identificacion','nombre','apellido','edad','direccion','telefono')
   
    search_fields=['id_cliente','nombre']
admin.site.register(Clientes,ClientesAdmin  )

class ventasAdmin(admin.ModelAdmin):
    list_display=('id_venta','fecha','costo','clientes')
    search_fields=['clientes','id_venta']
    list_filter=['clientes']
    
admin.site.register(Ventas,ventasAdmin)

class reservaAdmin(admin.ModelAdmin):
    list_display=('id_reserva','nombre','fecha','atracciones_reservas')
    search_fields=['atracciones_reservas','id_reserva']
    list_filter = ['atracciones_reservas']

admin.site.register(Reservas,reservaAdmin)

class EmpleadoAdmin(admin.ModelAdmin):
    list_display=('id_empleado','identificacion','nombre','apellido','correo')
    search_fields=['correo','apellido']

admin.site.register(Empleados,EmpleadoAdmin)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','usuario', 'correo', 'rol')
admin.site.register(Usuario, UsuarioAdmin)

class AvisoAdmin(admin.ModelAdmin):
    list_display=('id_aviso','nombre','imagen')
admin.site.register(Aviso,AvisoAdmin)


class Boletas_Producto_Admin(admin.ModelAdmin):
    list_display=('codigo_producto','nombre_boleta_producto','foto','precio','stock')
    search_fields=['nombre_boleta_producto']
admin.site.register(Boletas_producto,Boletas_Producto_Admin)

class PedidoAdmin(admin.ModelAdmin):
    list_display=('cliente','fecha','direccion_de_envio','estado')
    list_filter=['estado','fecha']
admin.site.register(Pedido,PedidoAdmin)

class PedidoProductoAdmin(admin.ModelAdmin):
    list_display=('id','pedido','producto','cantidad','precio')
    list_filter=['pedido']
    search_fields=['pedido']
admin.site.register(PedidoProducto,PedidoProductoAdmin)
# Register your models here.
