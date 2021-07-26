from collections import namedtuple
from django.urls import path

from.import  views
app_name='diverty'
urlpatterns=[
    #login
    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    
    path('',views.index,name='index'),
    path('formulario_login/',views.formulario_login,name='formulario_login'),
    path('formulario_register/',views.formulario_register,name='formulario_register'),
    path('registrar_usuario/',views.registrarUsuarios,name='registrar_usuario'),
    #clientes-urls:
    path('listar_clientes/',views.crud_clientes,name='listar_clientes'),
    path('agregar_clientes/',views.guardarClientes,name='agregar_clientes'),
    path('modificar_clientes/<int:id>/',views.modificarClientes,name='modificar_clientes'),
    path('eliminar-clientes/<int:id>/',views.eliminarClientes,name='eliminar-clientes'),
    
        #empleados urls:
    path('listado_empleado/',views.crud_empleado,name='listado_empleado'),
    path('guardar_empleado/',views.guardarEmpleado, name='guardar_empleado'),
    path('modificar_empleado/<int:id>/',views.editarEmpleado,name="modificar_empleado"),
    path('eliminar_empleado/<int:id>/', views.eliminarEmpleado,name='eliminar_empleado'),


    #ventas urls
    path('listar_ventas/',views.crud_ventas,name='listar_ventas'),
    path('guardar-ventas/',views.guardarVentas,name='guardar-ventas'),
    path ('modificar_ventas/<int:id>/',views.editarVentas,name='modificar_ventas'),
    path('eliminar_ventas/<int:id>/',views.eliminarVentas,name='eliminar_ventas'),
    #promociones urls
    path('listado_promociones/',views.crud_promociones,name='listado_promociones'),
    path('guardar_promociones/',views.guardarPromociones,name='guardar_promociones'),
    path('modificar_promociones/<int:id>/',views.editarPromociones,name='modificar_promociones'),
    path('eliminar_promociones/<int:id>/',views.eliminarPromociones,name='eliminar_promociones'),
  
    # atracciones urls
    path('listado_atracciones/',views.crud_atracciones,name='listado_atracciones'),
    path('guardar_atracciones/',views.guardarAtracciones,name='guardar_atracciones'),
    path('modificar_atracciones/<int:id>/',views.modificarAtracciones,name='modificar_atracciones'),
    path('eliminar_atracciones/<int:id>/',views.eliminarAtracciones,name='eliminar_atracciones'),


    #reservas urls
    path('listado_reservas/',views.crud_reservas,name='listado_reservas'),
    path('guardar_reservas/',views.guardarReservas,name='guardar_reservas'),
    path('modificar_reservas/<int:id>/',views.editarReservas,name='modificar_reservas'),
    path('eliminar_reservas/<int:id>/',views.eliminarReservas,name='eliminar_reservas'),

    #tienda urls
    path('tienda/',views.tienda,name="tienda"),
    path('agregar_carrito/<str:id>/',views.agregarCarrito,name='agregar_carrito'),
    path('carro/',views.verCarrito,name="carro"),
    path('quitar_producto/<str:id>/',views.quitarProducto,name='quitar_producto'),
    path('limpiar_carrito',views.limpiarCarrito,name='limpiar_carrito'),
    path('editar_carrito/<str:id>/<int:cantidad>/',views.editarCarrito,name='editar_carrito'),
    path('guardar_pedido',views.guardarPedido,name='guardar_pedido'),

    #usuarios
    path('usuarios/',views.crud_usuarios,name='usuarios'),
    path('form_usuario',views.usuarioformulario,name='form_usuario'),
    path('guardar_usuario/',views.guardarUsuario,name='guardar_usuario'),
    path('eliminar_usuario/<int:id>/',views.eliminarUsuarios,name='eliminar_usuario'),
    path('actualizar_usuario/<int:id>/',views.actualizarUsuarios,name='actualizar_usuario'),
    path('editar_usuario/',views.editarUsuarios,name='editar_usuario'),

    #aviso
    path('listar_aviso',views.crud_aviso,name='listar_aviso'),
    path('guardar_aviso/',views.guardarAviso,name='guardar_aviso'),
    path('modificar_aviso/<int:id>/',views.editarAviso,name='modificar_aviso'),
    path('eliminar_aviso/<int:id>/',views.eliminarAviso,name='eliminar_aviso'),

    #productos

    path('listar_productos',views.crud_productos,name='listar_productos'),
    path('guardar_productos',views.guardarProductos,name='guardar_productos'),
    path('modificar_productos/<int:id>/',views.editarProductos,name='modificar_productos'),
    path('eliminar_productos/<int:id>/',views.eliminarProductos,name='eliminar_productos'),

    #pedidos
    path('listar_pedidos/',views.crud_pedidos,name='listar_pedidos'),
    path('guardar_pedidos',views.guardarPedidos,name='guardar_pedidos'),
    path('editar_pedidos/<int:id>/',views.editarPedidos,name='editar_pedidos'),
    path('eliminar_pedidos/<int:id>/',views.eliminarPedidos,name='eliminar_pedidos'),
    path ('listar_productos_del_pedido/',views.crud_productos_pedido,name='listar_productos_del_pedido'),
    path('eliminar_detalles/<int:id>/',views.eliminarDetalles,name='eliminar_detalles')
    

 

    
   
]

