from django import http
from django.core import paginator
from django.db.models.query import FlatValuesListIterable, RawQuerySet
from django.db.utils import IntegrityError
from django.http import request
from django.http.request import host_validation_re
from django.http.response import Http404
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import  PedidoProducto, Promociones,Atracciones,Clientes,Ventas,Reservas,Empleados,Usuario,Aviso,Boletas_producto,Pedido
from .forms import ClienteForm,EmpleadoForm, ReservasForm,VentasForm,PromocionesForm,AtraccionesForm,AvisoForm,Boletas_productoForm,PedidoForm,PedidoProductoForm
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q


from django.contrib import messages
# Create your views here.
#Pagina princiapl
def index(request):
    # se crea un diccionario para obtener todas las instancias de  la tabla Avisos
    data= {
        'Aviso':Aviso.objects.all(),
    }
    return render (request,'diverty/index.html',data)
#vista personalizada 404

#formulario login
def formulario_login(request):
       #obtiene la session
    if request.session.get("login",False):
        #retorna al index en caso de que la session ya este iniciada
        return HttpResponseRedirect(reverse('diverty:index'))
    else:
        return render (request,'diverty/formulario_login.html')
#formulario register
def formulario_register(request):
    return render (request,'diverty/registro_usuarios.html')
def login (request):
    if request.method== 'POST':
        #este try lo que hace es que prueba todo lo que este dentro de este try
        try:
            # se crea la variable e en donde se va a alojar el valor del correo del atributo name del html
            e=request.POST['correo']
            # se crea la variable c en donde se va a alojar el valor de la contraseña del atributo name del html
            c=request.POST['contraseña']
            # se obtiene todos los objetos de tipo de usuario por medio de la variable usuarios y posteriormente se reemplazan  por lo que tenga el valor del name del html
            usuarios=Usuario.objects.get(correo=e,clave=c)
            # se obtiene  los datos de la sesion de usuarios
            request.session["login"]=[usuarios.id,usuarios.usuario,usuarios.rol,usuarios.correo]
            # se redigirge al index si todo sale bien
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        # en caso de que encuentre alguna excepcion  como que el usuario no exista,entonces:
        except Usuario.DoesNotExist:
            #manda el error
            messages.error(request,"Email  o contraseña incorrectos")
        #lo redirigira al mismo formulario
        return HttpResponseRedirect(reverse('diverty:formulario_login',args=()))
    else:
        # si se manda algo por get y no por post entonces lo redirecciona al index
        return HttpResponseRedirect(reverse('diverty:index'))
def logout(request):
    #verifica primero lo que este dentro del try
    try:
        carrito=request.session.get("carrito",False)
        bolsa=request.session.get("bolsa",False)


        if not carrito and not bolsa:
            del request.session["login"]
            messages.success(request,"Has salido satisfactoriamente")
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        else:

        #permite cerrar la session eliminando la session con el metodo del
            del request.session["login"]
            del request.session["carrito"]
            del request.session["bolsa"]
        # Manda un mensaje de cerrado satisfactoriamente
            messages.success(request,"Has salido satisfactoriamente")
        # redigire al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
    except:
        # en caso de que exista un problema suelta el siguiente mensaje
        return HttpResponse("Oh no,ocurrio un error")

def registrarUsuarios(request):
    #  evalua  primero lo que está dentro del try
    try:
        #en caso de que el formulario se vaya por el metodo post
        if request.method=='POST':
            # si el valor del name del input del html de clave es igual al de clave2 entonces:
            if request.POST['clave']==request.POST['clave2']: 
                # se crea una instancia de tipo usuario
                u=Usuario(
                    #el campo usuario de la base de datos sera igual al valor que tenga  el name de usuario en el input de este mismo
                    usuario=request.POST['usuario'],
                    #el campo email de la base de datos sera igual al valor que tenga  el name de email en el input de este mismo
                    correo=request.POST['email'],
                    #el campo clave de la base de datos sera igual al valor que tenga  el name de password en el input de este mismo
                    clave=request.POST['clave'],
                )
                #se guarda el formulario
                u.save()
                #se envia un mensaje de proceso satisfactorio
                messages.success(request,"Usuario registrado correctamente")
                # si todo sale bien se retorna al index
                return HttpResponseRedirect(reverse('diverty:index',args=()))
            else:
                # en caso de que haya un error se muestra el mensaje de que las claves no concuerdan
                error=messages.error(request,"Las contraseñas no coinciden ")
                return HttpResponseRedirect(reverse('diverty:formulario_register',error))     
        else:
            #en caso de que vaya por metodo get se devuelve el mensaje de fin
            return HttpResponse("fin")
    #si hay una excepcion de tipo integrity error mostrara el siguiente mensaje:
    except IntegrityError:
        messages.error(request,'El usuario o el email o los dos ya se encuentran registrados')
    #retornara al formulario de register    
    return HttpResponseRedirect(reverse("diverty:formulario_register",args=()))
def crud_usuarios(request):
    session=request.session.get("login",False)
    if session and (session[2] ==1 or session[2] ==2):
        # obtiene los objetos de tipo de cliente
        registros_tablas=Usuario.objects.all() 
        # crea una instancia de tipo paginator en donde  se le indica a que instancia quiere utilizar y cuantos registos por pagina
        paginator=Paginator(registros_tablas,4)
        # rescata el numero de paginas al interactuar el usuario con la paginacion
        page=request.GET.get('page') or 1
        # se sobreescribe la variable registros_tablas para que se obtengan todos los clientes que esten dentro de la variable page que a su vez contiene el numero de la pagina en que se encuentra ubicado el usuario 
        registros_tablas=paginator.get_page(page) 
        # permite que ese numero de pagina que se pasa como string mediante el get en la url del navegador se convierta a int con el proposito de hacer un for que vaya contando y imprimiendo el numero de paginas que se necesita y que en caso de que una pagina supere las 4 que vienen por defecto este se incremente en 1 nueva pagina
        paginactual=int(page)
        # permite hacer un contador desde el methodo range que permite ir desde el 1 que es la primer pagina hasta el numero de pagina en que se ubica el usuario + la siguiente esto con el fin de que el usuario pueda interactuar con la actual y siguiente página a la que le vaya a dar click.
        paginas=range(1,registros_tablas.paginator.num_pages+1)
        data={
            'registros_tablas':registros_tablas,
             #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginas':paginas,
            #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginactual':paginactual 
        }
    else:
        return HttpResponseRedirect(reverse('diverty:index'))
    # renderizado del html  con el diccionario pasado como parametro para listar los objetos de tipo cliente y implementar las funcionalidades del páginado
    return render (request,'diverty/crud_usuarios.html',data) 
def usuarioformulario(request):
    #se obtiene la variable de session
    session=request.session.get("login",False)
    # pregunta por medio de un if si la session es administrador o cliente
    if session and (session[2] ==1 or  session[2] ==2):
        # returna al html si la session es correcta
        return render (request,'diverty/guardar_usuarios.html')
    else:
        # si la session no es correcta retorna al index
        return HttpResponseRedirect(reverse('diverty:index'))
def guardarUsuario(request):
    #captura la session
    session=request.session.get("login",False)
     # pregunta por medio de un if si la session es administrador o cliente
    if session and (session[2] ==1 or session[2] ==2):
        #evalua lo que hay en el try primero
        try:
            if request.method=='POST':
                if request.POST["roles"]=="":
                    messages.error(request,"Ingrese un rol")
                    return HttpResponseRedirect(reverse("diverty:form_usuario"))

                #si el metodo es post entonces pregunta si las dos contraseñas son iguales
                if request.POST['clave']==request.POST['clave']:
                    # de serlo se crea una instancia de tipo usuario en donde se va a guardar los datos que vienen del html a los campos en la base de datos
                    u=Usuario(
                        usuario=request.POST['usuario'],
                        correo=request.POST['email'],
                        clave=request.POST['clave'],
                        rol=request.POST['roles'],
                    )
                    #lo guarda si todo sale bien
                    u.save()
                    #manda un mensaje satisfactorio
                    messages.success(request,"usuario registrado correctamente")
                    #retorn a al index
                    return HttpResponseRedirect(reverse('diverty:usuarios',args=()))
                else:
                    #manda un mensaje de error si las contraseñas no coinciden
                    error=messages.error(request,"las contraseñas no coincide")
                #retorna al formulario de usuario
                return HttpResponseRedirect(reverse('diverty:form_usuario',error))
            else:
                # si se envia por get el formulario,muestra el mensaje de fin
                return HttpResponse("fin")
     
        except IntegrityError:
            #si hay una excepcion tipo IntegrityError muestra el  siguiente mensaje
            messages.error(request,'el email ya se encuenta registrado')
            #retorna  al index
            return HttpResponseRedirect(reverse("diverty:form_usuario",args=()))
    else:
        return HttpResponseRedirect(reverse('diverty:index'))     
def eliminarUsuarios(request,id):
    try:
        #obtiene la session
        session=request.session.get("login",False)
        #en caso de que la session sea administrador o cliente permitira eliminar un cliente
        if session and (session[2] ==1 or session[2] ==2):
            #se obtiene el id del usuario  de la instancia de usuario
            usuarios=Usuario.objects.get(pk=id)
            if session[0]==usuarios.id or session[2]==2 and usuarios.rol==1:
                return HttpResponseRedirect(reverse('diverty:index'))
            else:
            # elimina el registro
                usuarios.delete()
            #muestra el mensaje
                messages.success(request,"Usuario eliminado correctamente")     
        else:
            #en caso de que la session sea de cliente lo redirigira al index
           return HttpResponseRedirect(reverse('diverty:index',args=()))
    except IntegrityError:
        messages.error(request,"Elimine primero los pedidos asociados a este usuario")
    except Clientes.DoesNotExist:
        #muestra el siguiente mensaje si el cliente no existe
        messages.error(request,"No se encontrado el cliente "+str(id))
    #retorna al listado de usuarios despues de mostrar el mensaje
    return HttpResponseRedirect(reverse('diverty:usuarios')) 
def actualizarUsuarios(request,id):
    #obtiene la session
    session=request.session.get("login",False)
    #en caso de que la session sea administrador o cliente permitira eliminar un usuario
    if session and (session[2] ==1 or session[2] ==2):
        #captura el id del usuario para poder actualizarlo
        q=Usuario.objects.get(pk=id)
        # se pasa ese id por medio de un diccionario
        contexto={'datos':q}
        #renderiza el formulario de usuario con los datos que contenga ese id
        return render (request,'diverty/actualizar_usuario.html',contexto)
    else:
        # si la session es por el contrario de cliente,lo redirigira al index
        return HttpResponseRedirect(reverse('diverty:index'))
def editarUsuarios(request):
    try:
        if request.method == "POST":

            # se crea una variable llamada id donde contendra  el valor del name del html
            id = request.POST['id']
            # se crea una variable llamada nom donde contendra  el valor del name del html
            nom = request.POST['usuario']
            # se crea una variable llamada email donde contendra  el valor del name del html
            email = request.POST['email']
            # se crea una variable llamada rol_usuario donde contendra  el valor del name del html
            rol_usuario = request.POST['rol_tipo_usuario']
            # se crea una variable llamada q donde se obtendra el id de ese usuario para poder acceder a los distintos campos de ese usuario
            q = Usuario.objects.get(pk=id)
            # se manda a llamar a ese campo usuario de la base de datos y se le asigna la variable nom que contendra el name del html
            q.usuario = nom
            # se manda a llamar a ese campo correo de la base de datos y se le asigna la variable email que contendra el name del html
            q.correo = email
                # se manda a llamar a ese campo rol de la base de datos y se le asigna la variable rol_usuario que contendra el name del html
            q.rol = rol_usuario
            q.save()    #actualizar

            return HttpResponseRedirect(reverse('diverty:usuarios', args=()))#retorna al listado de usuarios
        else:
            return HttpResponseRedirect(reverse('diverty:index'))#retorna al index
    except IntegrityError:
        messages.error(request,"El email ya se encuentra registrado")
        return HttpResponseRedirect(reverse("diverty:editar_usuario"))


"""Lógica de clientes """
def crud_clientes(request):
    session=request.session.get("login",False)#Obtiene la session
    # si la session que se está manejando es de administrador o clientes entonces podra entrar al listado
    if session and (session[2] == 1 or session[2] == 2): 
        registros_tablas=Clientes.objects.all() # obtiene los objetos de tipo de cliente
        # crea una instancia de tipo paginator en donde  se le indica a que instancia quiere utilizar y cuantos registos por pagina
        paginator=Paginator(registros_tablas,4)
        # rescata el numero de paginas al interactuar el usuario con la paginacion
        page=request.GET.get('page') or 1 
        # se sobreescribe la variable registros_tablas para que se obtengan todos los clientes que esten dentro de la variable page que a su vez contiene el numero de la pagina en que se encuentra ubicado el usuario
        registros_tablas=paginator.get_page(page) 
        # permite que ese numero de pagina que se pasa como string mediante el get en la url del navegador se convierta a int con el proposito de hacer un for que vaya contando y imprimiendo el numero de paginas que se necesita y que en caso de que una pagina supere las 4 que vienen por defecto este se incremente en 1 nueva pagina
        paginactual=int(page)
        # permite hacer un contador desde el methodo range que permite ir desde el 1 que es la primer pagina hasta el numero de pagina en que se ubica el usuario + la siguiente esto con el fin de que el usuario pueda interactuar con la actual y siguiente página a la que le vaya a dar click.
        paginas=range(1,registros_tablas.paginator.num_pages+1)
        data={
            'registros_tablas':registros_tablas,
            #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginas':paginas, 
            #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginactual':paginactual 
    }
        # renderizado del html  con el diccionario pasado como parametro para listar los objetos de tipo cliente y implementar las funcionalidades del páginado
        return render (request,'diverty/crud_clientes.html',data) 
    else:
        # en caso de que la session no sea  ni la del administrador ni la del empleado lo redirigira al index
        return HttpResponseRedirect(reverse('diverty:index',args=()))   
#Gurdado de clientes
def guardarClientes(request):
    session=request.session.get("login",False)#Obtiene la session
    # en caso de que la session sea de administrador o empleado entonces permitira guardar clientes
    if session and(session[2] == 1 or session[2] == 2):
        data={
            'form':ClienteForm() #crea un diccionario con los campos del formulario
    }
    else:
        # en caso de que la session sea de cliente lo redirigira al index
        return HttpResponseRedirect(reverse ('diverty:index',args=()))
    if request.method=='POST':
        #permite rellenar el formulario con los datos introducidos
        formulario=ClienteForm(data=request.POST)
        if formulario.is_valid(): 
            formulario.save()# posteiormente guardara el formulario
            messages.success(request,"Cliente registrado")# entregara un mensaje de que el cliente  se registro correctamente
            # al guardar satisfactoriamente el formulario lo redirigira  al listado de clientes
            return HttpResponseRedirect(reverse('diverty:listar_clientes'))
        else:
            data["form"]=formulario #envia otra vez el formulario con los errores que salieron 
    # permite crear el formulario  y el data trae todos los campos del formulario que se generaran
    return render (request,'diverty/formulario_clientes.html', data) 
    
def modificarClientes(request, id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # en caso de que la session sea de administrador o cliente podra modificar los clientes
        if session and (session[2] ==1 or session[2] ==2):
            clientes=Clientes.objects.get(pk=id)#obtiene el id de ese cliente
            data={
            # se crea un diccionario que  crea un formulario con los objetos que se pasen como instance de clientes
            'form':ClienteForm(instance=clientes)
        }
        else:
            # en caso de que la session sea de cliente lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST': 
            # permite la visualicion de lo que se traiga de la instancia de tipo cliente y luego guardara lo que modifique el usuario con la variable data
            formulario=ClienteForm(data=request.POST,instance=clientes)
            if formulario.is_valid():
                formulario.save()#guarda el formulario
                messages.success(request,"Modificado correctamente")#muestra el mensaje satisfactorio
                # en caso de que todo salga bien redirigira al listado de clientes
                return HttpResponseRedirect(reverse('diverty:listar_clientes'))
            else:
                # si algo sale mal en el formulario lo volvera a rellenar  con los datos que ingreso mal el usuario
                data["form"]=formulario
    except Clientes.DoesNotExist:
        #devuelve este mensaje si el cliente no existe
        messages.error(request,"No existe el cliente :"+str(id))
        #lo redirigire al listado de clientes
        return HttpResponseRedirect(reverse('diverty:listar_clientes'))
    #permite la visualizacion de los datos del formulario a la hora de editar
    return render (request,'diverty/modificar_clientes.html',data)
#Eliminar Clientes
def eliminarClientes(request, id):
    try:
        session=request.session.get("login",False)#obtiene la session
        #en caso de que la session sea administrador o cliente permitira eliminar un cliente
        if session and (session[2] ==1 or session[2] ==2):
            #se obtiene el id cliente llamando a la  tabla de clientes
            clientes=Clientes.objects.get(pk=id)
            clientes.delete()# elimina el registro
            messages.success(request,"Cliente eliminado correctamente")#muestra un mensaje  
        else:
        #en caso de que la session sea de cliente lo redirigira al index
           return HttpResponseRedirect(reverse('diverty:index',args=()))
    except IntegrityError:
        #muestra este mensaje si la excepcion es tipo integrityError
        messages.error(request,"Existen ventas asociadas a estos clientes,elimine primero las ventas")
    except Clientes.DoesNotExist:
        messages.error(request,"No se encontrado el cliente "+str(id))#muestra este mensaje si la excepcion es tipo Cliente no existe
    return HttpResponseRedirect(reverse('diverty:listar_clientes'))   #retorna al listado de clientes
"""Fin lógica de clientes"""

"""Lógica de empleado"""
def crud_empleado(request):
    session=request.session.get("login",False)#captura la session
    # if que permite  evaluar si se deja mostrar por url el listado en caso de que el rol sea administrador o empleado
    if session and (session[2] ==1):
        registros_tablas=Empleados.objects.all() # obtiene los objetos de tipo de cliente
        # crea una instancia de tipo paginator en donde  se le indica a que instancia quiere utilizar y cuantos registos por pagina
        paginator=Paginator(registros_tablas,4)
        page=request.GET.get('page') or 1 # rescata el numero de paginas al interactuar el usuario con la paginacion
        # se sobreescribe la variable registros_tablas para que se obtengan todos los empleados que esten dentro de la variable page que a su vez contiene el numero de la pagina en que se encuentra ubicado el usuario
        registros_tablas=paginator.get_page(page) 
        # permite que ese numero de pagina que se pasa como string mediante el get en la url del navegador se convierta a int con el proposito de hacer un for que vaya contando y imprimiendo el numero de paginas que se necesita y que en caso de que una pagina supere las 4 que vienen por defecto este se incremente en 1 nueva pagina
        paginactual=int(page)
        # permite hacer un contador desde el methodo range que permite ir desde el 1 que es la primer pagina hasta el numero de pagina en que se ubica el usuario + la siguiente esto con el fin de que el usuario pueda interactuar con la actual y siguiente página a la que le vaya a dar click.
        paginas=range(1,registros_tablas.paginator.num_pages+1)
        data={
            'registros_tablas':registros_tablas,
            #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginas':paginas, 
            #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginactual':paginactual 
        
    }
    else:
        #en caso de que la session sea de tipo empleado o clientes entonces lo redirigira al index
        return HttpResponseRedirect(reverse('diverty:index',args=()))
    #renderiza el formulario con el diccionario
    return render (request,'diverty/listado_empleado.html',data)
    
def guardarEmpleado(request):
    session=request.session.get("login",False)#obtiene la session
    # if que permite  evaluar si se deja mostrar por url el listado en caso de que el rol sea administrador o empleado
    if session and (session[2] ==1):
        data={
            'form':EmpleadoForm()# crea una instancia de tipo formulario
    }
    else:
        # en caso de que la session sea empleado o cliente entonces lo redigira al index
        return HttpResponseRedirect(reverse('diverty:index',args=()))
    if request.method=='POST':
        formulario=EmpleadoForm(data=request.POST)#obtiene todos los datos que pase el usuario en el formulario
        if formulario.is_valid():
            formulario.save()#guarda el formulario
            messages.success(request,'Empleado registrado')#envia un mensaje
            # en caso de que todo salga bien lo redirigira al listado de empleado
            return HttpResponseRedirect(reverse('diverty:listado_empleado'))
        else:
            # en caso de que haya un error devuelve el formulario con los datos erroneos
            data["form"]=formulario
    #renderiza  el html y el diccionario data permite crear los campos correspondientes en el html
    return render (request,'diverty/formulario_empleado.html',data)

def editarEmpleado(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        if session and (session[2] ==1):#si la session es de administrador entonces solo el podra editar un empleado
            empleados=Empleados.objects.get(pk=id)# obtiene el id del empleado
            data={
                # crea y rellena el formulario con el registro original que se trae de la base de datos
                'form':EmpleadoForm(instance=empleados)
        }
        else:
            # en caso de que la session sea de empleado o cliente lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST':
            # permite la visualizacion de lo que se traiga de la instancia de tipo empleado y luego guardara lo que modifique el usuario con la variable data
            formulario=EmpleadoForm(data=request.POST,instance=empleados)
            if formulario.is_valid():
                formulario.save()#guarda el formulario
                messages.success(request,"Modificado correctamente")#envia un mensaje
                return HttpResponseRedirect(reverse('diverty:listado_empleado'))#retorna al listado de empleado
            else:
                # si algo sale mal rellenara el formulario con los datos errores que se ingresaron
                data["form"]=formulario
    except Empleados.DoesNotExist:
        #muestra el siguiente mensaje si el empleado no existe
        messages.error(request,"No existe el empleado "+str(id))
        return HttpResponseRedirect(reverse('diverty:listado_empleado'))#retorna al listado de empleados
    #renderiza  el html y el diccionario data permite crear los campos correspondientes en el html   
    return render (request,'diverty/modificar_empleado.html',data)   
    
def eliminarEmpleado(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # en caso de que la session sea de administrador entonces solo el podra eliminar un empleado
        if session  and(session[2] ==1):
            empleados=Empleados.objects.get(pk=id)#se obtiene el id del empleado a eliminar
            empleados.delete()#lo elimina
            messages.success(request,' Empleado eliminado correctamente')#envia un mensaje
        else:
            # en caso de que la session sea de empleado o cliente los redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
    except Empleados.DoesNotExist:
        #muestra el siguiente mensaje si el empleado no existe
        messages.error(request,"No se ha encontrado el  empleado: " +str(id))
    #redirecciona al listado de empleado
    return HttpResponseRedirect(reverse('diverty:listado_empleado'))
      
""" Fin logica de empleados"""


"""Lógica de ventas """
def crud_ventas(request):
    session=request.session.get("login",False)#obtiene la session
    # si el rol es administrador o empleado entonces podra ver el listado de ventas
    if session and (session[2] ==1 or session[2] ==2):
        registros_tablas=Ventas.objects.all()#Obtiene todos los objetos de tipo ventas
        # crea una instancia de tipo paginator en donde  se le indica a que instancia quiere utilizar y cuantos registos por pagina
        paginator=Paginator(registros_tablas,4)
        # rescata el numero de paginas al interactuar el usuario con la paginacion
        page=request.GET.get('page') or 1
        # se sobreescribe la variable registros_tablas para que se obtengan todas las ventas que esten dentro de la variable page que a su vez contiene el numero de la pagina en que se encuentra ubicado el usuario
        registros_tablas=paginator.get_page(page)
        # permite que ese numero de pagina que se pasa como string mediante el get en la url del navegador se convierta a int con el proposito de hacer un for que vaya contando y imprimiendo el numero de paginas que se necesita y que en caso de que una pagina supere las 4 que vienen por defecto este se incremente en 1 nueva pagina
        paginactual=int(page)
            # permite hacer un contador desde el methodo range que permite ir desde el 1 que es la primer pagina hasta el numero de pagina en que se ubica el usuario + la siguiente esto con el fin de que el usuario pueda interactuar con la actual y siguiente página a la que le vaya a dar click.
        paginas=range(1,registros_tablas.paginator.num_pages+1)

        data={
            'registros_tablas':registros_tablas,# crea un diccionario con esos objetos
            'paginas':paginas,
            'paginactual':paginactual
    }
    else:
        return HttpResponseRedirect(reverse('diverty:index',args=()))# en caso de que la session sea de cliente lo redirigira al index
    return render (request,'diverty/listar_ventas.html',data)# los pasa como parametro para visualizar el listado de registros

def guardarVentas(request):
    session=request.session.get("login",False)#obtiene la session
    # en caso de que la session sea de administrador o empleado podra guardar una venta
    if session and (session[2] ==1 or session[2] ==2):
        data={
            'form':VentasForm()# crea una instancia del formulario
    }
    else:
        return HttpResponseRedirect(reverse("diverty:index",args=()))# en caso de que la session sea de clientes lo redirigira al index
    if request.method=='POST':
        formulario=VentasForm(data=request.POST)# obtiene los datos que ingreso el usuario al formulario y los guarda
        if formulario.is_valid():
            formulario.save()#guarda el formulario
            # en caso de que todo este totalmente correcto redirige al usuario al listado de ventas
            return HttpResponseRedirect(reverse('diverty:listar_ventas'))
        else:
            data["form"]=formulario# en caso de que no,devuelve todos los datos que ingreso el usuario con sus respectivos errores 
    #renderiza el formulario html y  pasa los datos ingresados del usuario por medio del diccionario data
    return render (request,'diverty/formulario_ventas.html',data)

def editarVentas(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # en caso de que la session sea de administrador o empleado entonces podra editar una venta
        if session and(session[2] ==1 or session[2] ==2):
            ventas=Ventas.objects.get(pk=id)#obtiene el id de la venta para poder editarla
            data={
                #crea la instancia del formulario y pasa por medio de una instancia los objetos que esten contenidos en la variable de tipo ventas
                'form':VentasForm(instance=ventas)
        }
        else:
            #en caso de que la session sea de cliente entonces lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST':
            # el diccionario data guarda lo que vaya a modificar el usuario y la instance permite visualizar los registros originales en el html
            formulario=VentasForm(data=request.POST,instance=ventas)
            if formulario.is_valid():
                formulario.save()#guarda el formulario
                messages.success(request,"Modificado correctamente")#envia un mensaje
                #en caso de que todo salga correcto lo redirige al listado de ventas
                return HttpResponseRedirect(reverse('diverty:listar_ventas'))
            else:
                #si el formulario no es correcto,lo rellena y lo vuelve a mostrar con los datos erroneos
                data["form"]=formulario
    except Ventas.DoesNotExist:
        #muestra este mensaje si una venta no existe
        messages.error(request,"No existe la venta "+str(id))    
        #lo redirige al listado de ventas
        return HttpResponseRedirect(reverse('diverty:listar_ventas'))
    # se renderiza el formulario con el diccionario del data
    return render (request,'diverty/modificar_ventas.html',data)
  
def eliminarVentas(request,id):
    try:
        session=request.session.get("login",False)#Obtiene la session
        # si la session es de administrador o empleado  podra eliminar una venta
        if session and (session[2] ==1 or session[2] ==2):
            #Obtiene el id de la venta 
            ventas=Ventas.objects.get(pk=id)
            ventas.delete()#con este metodo se eliminara la venta
            messages.success(request,"Venta eliminada correctamente")#mensaje de eliminado satisfactoriamente
        else:
            return HttpResponseRedirect(reverse('diverty:index',args=()))# en caso de que la session sea del cliente lo redirigira al index
    except Ventas.DoesNotExist:
        #entregara este mensaje si la venta no existe
        messages.error(request,"No existe la venta :"+str(id))
    return  HttpResponseRedirect(reverse('diverty:listar_ventas'))#en caso de que se elimine se redirigira al listado de ventas

"""Fin lógica de ventas"""
"""Lógica de promociones"""
#crud promociones
def crud_promociones(request):
    session=request.session.get("login",False)#obtiene la session
    # en caso de que la session  sea del administrador o empleado podra listar las promociones
    if session and (session[2] ==1 or session[2] ==2):
        registros_tablas=Promociones.objects.all()#obtiene todos los registros de promociones
        #por medio de la variable paginator crea un metodo paginator que permitira saber  que vamos a paginar y de cuanto en cuanto vamos a paginar
        paginator=Paginator(registros_tablas,4)
        page=request.GET.get('page') or 1#rescata el numero de paginas que se muestra por la url
        #sobreescribe la variable registros_tablas para obtener los registros de promociones que esten en cada pagina
        registros_tablas=paginator.get_page(page)
        #convierte el string del numero de pagina en un int para despues calcular el conteo de paginas y poder agregar otra en caso de que se necesite
        paginactual=int(page)
        # gracias al range va desde el primer registro hasta el ultimo y en caso de que llegue al maximo de registros por pagina,o sea 4,incrementa en una nueva pagina
        paginas=range(1,registros_tablas.paginator.num_pages+1)
        data={
            'registros_tablas':registros_tablas,#se pasa por medio de un diccionario esta variable para que se pueda obtener todos los registros de cada una de las paginas
            'paginactual':paginactual,#se pasa esta variable para posteriormente hacer el calculo para una pagina nueva
            'paginas':paginas
    }
    else:
        # en caso de que la session sea de cliente,entonces lo redirigira al index
        return HttpResponseRedirect(reverse('diverty:index',args=()))
    #renderiza el html y pasa el diccionario de data para que se pueda mostrar el listado de promociones y se pueda paginar
    return render (request,'diverty/listado_promociones.html',data)

#formulario promociones
def guardarPromociones(request):
    session=request.session.get("login",False)#obtiene la session
    # si la sessione es administrador o empleado dejara  guardar una promocion
    if session and (session[2] ==1 or session[2] ==2):
        data={
            'form':PromocionesForm()# crea  una instancia de promociones que se va a traer el formulario ya hecho 
    }
    else:
        # en caso de que la session sea de usuario entonces retornara al index
        return HttpResponseRedirect(reverse("diverty:index",args=()))
    if request.method=='POST':
        formulario=PromocionesForm(data=request.POST)#el formulario creado recogera  todos los datos del usuario
        if formulario.is_valid():# en caso de que el formulario sea valido,entonces:
            formulario.save()#guardar el formulario
            return HttpResponseRedirect(reverse('diverty:listado_promociones'))#lo redirige al listado de promociones
        else:
            data["form"]=formulario# si el formulario no es valido,se rellenara y mostra con los campos erroneos
    #renderiza el formulario y se trae el data  que es el que va a contener todos los datos del formulario
    return render (request,'diverty/formulario_promociones.html',data)

def editarPromociones(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # sila session es administrador o empleado entonces permitira editar una promocion
        if session and (session[2] ==1 or session[2] ==2):
            promociones=Promociones.objects.get(pk=id)#captura el id de la promocion a editar
            data={
                'form':PromocionesForm(instance=promociones)#creara un formulario  con el id que se le pase
        }
        else:
            # en caso de que la session sea de un cliente lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST':
            #permitira imprimir el contenido del registro antiguo y guardar el contenido del nuevo registro
            formulario=PromocionesForm(data=request.POST,instance=promociones)
            if formulario.is_valid():# en caso de que el formulario sea valido:
                formulario.save()#guarda el formulario
                messages.success(request,"Modificado correctamente")#muestra un mensaje de que se ha creado correctamente
                return HttpResponseRedirect(reverse('diverty:listado_promociones'))# redirige al listado de promociones
            else:
                data["form"]=formulario#si el formulario no es valido,lo rellenara y lo mostrara con los datos erroneos
    except Promociones.DoesNotExist:
        #muestra este mensaje si la promocion no existe
        messages.error(request,"No existe la promocion :"+str(id))
        #retorna al listado de promociones
        return HttpResponseRedirect(reverse('diverty:listado_promociones'))
    #renderiza el formulario con los datos de la variable data para mostrarlo ya lleno
    return render (request,'diverty/modificar_promociones.html',data)
    
def eliminarPromociones(request,id):
    try:
        session=request.session.get("login",False)# obtiene  la session
        # en caso de que la session  sea del administrador o empleado podra eliminar una promcoion
        if session and (session[2] ==1 or session[2] ==2):
            promociones=Promociones.objects.get(pk=id)#captura el id de la promocion a eliminar
            promociones.delete()#lo elimina
            messages.success(request,"eliminado correctamente")# entrega un mensaje    
        else:
            # en caso de que la session sea del cliente lo redirigira al index
            return HttpResponseRedirect(reverse("diverty:index",args=()))
    except IntegrityError:
        messages.error(request,"Error,primero elimine o modifique el registro o campo de descuento de los los productos asociados a esta promocion")
    except Promociones.DoesNotExist:
        #muestra el siguiente mensaje si la promocion no existe
        messages.error(request,"No existe la promocion "+str(id))

    return HttpResponseRedirect(reverse('diverty:listado_promociones'))# lo redirige al listado de promociones
#crud atracciones
def crud_atracciones(request):
    session=request.session.get("login",False)#obtiene la session
    #si la session es del administrador o empleado entonces podra ver el listado de atracciones
    if session and (session[2] ==1 or session[2] ==2):

        registros_tablas=Atracciones.objects.all()#se trae todos los registros de atracciones
        paginator=Paginator(registros_tablas,4)#va a mostrar por pagina 4  registros de atracciones
        page=request.GET.get('page') or 1#rescata el numero de paginas
        #sobreescribe registros_tablas pero con ello se traera todos los registros de cada pagina de atracciones
        registros_tablas=paginator.get_page(page)
        paginactual=int(page)#convierte el numero de paginas a int
        paginas=range(1,registros_tablas.paginator.num_pages+1)#permite incrementar a una pagina si pasa el limite que es de 4

        data={
            'registros_tablas':registros_tablas,
            'paginactual':paginactual,
            'paginas':paginas
    }
    else:
        return HttpResponseRedirect(reverse("diverty:index",args=()))# en caso de que la session sea de clientes lo redirigira al index
    return render (request,'diverty/listado_atracciones.html',data)#renderiza el listado y se trae todos los datos de atracciones
#formulario atracciones
def guardarAtracciones(request):
    session=request.session.get("login",False)#obtiene la session
    if session and (session[2] ==1 or session[2] ==2):# si la session es administrador o empleado permitira guardar la atraccion
        data={
            'form':AtraccionesForm()#crea una instancia del formulario  de atracciones que contendra todos los campos de esa tabla
    }
    else:
        return HttpResponseRedirect(reverse('diverty:index',args=()))# en caso de que la session sea de cliente lo redirigira al index
    if request.method=='POST':
        formulario=AtraccionesForm(data=request.POST)#captura los datos enviados por el usuario
        if formulario.is_valid():#valida si el formulario es valido
            formulario.save()#lo guarda si es valido
            messages.success(request,"Atraccion guardada correctamente")
            return HttpResponseRedirect(reverse('diverty:listado_atracciones'))# lo redirige al listado de atracciones
        else:
            data["form"]=formulario#en caso de que haya algun error rellena el formulario con los errores correspondientes
    #renderiza el formulario y el data permite visualizar los campos del formulario
    return render (request,'diverty/formulario_atracciones.html',data)
def modificarAtracciones(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # si la session es de administrador o empleado permitira modificar  las atracicones
        if session and (session[2] ==1 or session[2] ==2):
            atracciones=Atracciones.objects.get(pk=id)#obtiene el id de la atraccion a modificar
            data={
                'form':AtraccionesForm(instance=atracciones)#crea el formulario y se trae el id de la variable atracciones
        }
        else:
            # en caso de que la session sea de clientes lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST':
            #permitira rellenar el formulario con los datos antiguos y tambien permitira editarlos con los datos que añada el usuario
            formulario=AtraccionesForm(data=request.POST,instance=atracciones)
            if formulario.is_valid():# si el formulario es valido,entonces:
                formulario.save()#guarda el formulario
                messages.success(request,"modificado correctamente")#muestra un mensaje
                return HttpResponseRedirect(reverse('diverty:listado_atracciones'))# lo redirige al listado de atracciones
            else:
                # en caso de que algo salga mal,rellena el formulario con los errores correspondientes que salieron
                data["form"]=formulario
    except Atracciones.DoesNotExist:
        #muestra el siguiente mensaje si una atraccion no se encontro
        messages.error(request,"La atraccion con id "+str(id)+ " no fue encontrada ")
        return HttpResponseRedirect(reverse('diverty:listado_atracciones'))# lo redirige al listado de atracciones
    #renderiza el formulario y la data se traera todos  los campos y los datos del registro
    return render (request,'diverty/modificar_atracciones.html',data)
def eliminarAtracciones(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # en caso de que la session sea de administrador o empleado entonces podra eliminar una atraccion
        if session and (session[2] ==1 or session[2] ==2):

            atracciones=Atracciones.objects.get(pk=id)#captura el id de la atraccion
            atracciones.delete()# eliminara el registro
            messages.success(request,"Eliminado correctamente ")#mostrara el mensaje
        else:
            # en caso de que la session sea  de cliente entonces lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
    except Atracciones.DoesNotExist:
        #mostrara el siguiente mensaje si no encuentra una atraccion a la hora de eliminar
        messages.error(request,"No se encontro la atraccion con id "+str(id))
    return HttpResponseRedirect(reverse('diverty:listado_atracciones'))# lo redirigira al listado de promociones
"""fin lógica de atracciones"""
def crud_reservas(request):
    session=request.session.get("login",False)#obtiene la session
    # si la session es de administrador o empleado entonces permitira listar las reservas
    if session and (session[2] ==1 or session[2] ==2):
        registros_tablas=Reservas.objects.all()# obtiene todos los registros de tipo reserva
        paginator=Paginator(registros_tablas,4)#pagina los registros de tipo reserva en 4
        page=request.GET.get('page') or 1#rescata el numero de paginas de la url
        #sobreescribe la variable registros_tablas pero con el fin de traerse los registros de reservas por cada pagina que haya
        registros_tablas=paginator.get_page(page)
        paginactual=int(page)#convierte  las paginas que son string a int
        #permite  incrementar el numero de paginas en caso de que se haya sobrepasado el numero de registros por pagina maximo
        paginas=range(1,registros_tablas.paginator.num_pages+1)
        data={#crea un diccionario con los datos que le tenemos que entregar al html para que liste las reservas y haga el paginado
            'registros_tablas':registros_tablas,
            'paginactual':paginactual,
            'paginas':paginas,

    }
    else:
        # en caso de que la session sea de cliente entonces lo redirigira al index
        return HttpResponseRedirect(reverse('diverty:index',args=()))
    #renderiza el listado y se trae todos los datos para mostrar las reservas y para poder interactuar con el paginado
    return render(request,'diverty/listado_reservas.html',data)


def guardarReservas(request):
    session=request.session.get("login",False)#obtiene la session
    if session and (session[2] ==1 or session[2] ==2):# si la session es de administrador o empleado permite guardar una reserva
        data={
            "form":ReservasForm()#crea una instancia de reservas que es el formulario con todos los campos que necesita
    }
    else:
        return HttpResponseRedirect(reverse('diverty:index',args=()))# en caso de que la session sea de cliente lo redirige al index
    if request.method=='POST':
        formulario=ReservasForm(data=request.POST)#captura todos los datos introduccidos por el usuario
        if formulario.is_valid():# si el formulario es valido,entonces:
            formulario.save()#guarda el formulario
            messages.success(request,"Guardado correctamente ")#muestra el mensaje
            return HttpResponseRedirect(reverse('diverty:listado_reservas'))#lo redirige al listado de reservas
        else:
            # en caso de que algo haya salido mal,rellena el formulario con todos los datos erroneos que salieron
            data["form"]=formulario
    # renderiza el formulario de reservas y el data permite tanto mostrar los campos de dicho formulario como poder guardar con los datos que ingrese el usuario
    return render (request,'diverty/formulario_reservas.html',data)
                
def editarReservas(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # si la session es del administrador o empleado entonces podra editar una reserva
        if session and (session[2] ==1 or session[2] ==2):
            reservas=Reservas.objects.get(pk=id)#obtiene el id de la reserva
            #crea un diccionario que contrenda los campos de dicho formulario que correspondan al id
            data={
                "form":ReservasForm(instance=reservas)
        }
        else:
            # en caso de que la session sea de usuario entonces lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST':
            #permite llenar el formulario con los datos que correspondan al id y permite modificar los datos
            formulario=ReservasForm(data=request.POST,instance=reservas)
            if formulario.is_valid():#si el formulario es valido,entonces
                formulario.save()#guardar el formulario
                messages.success(request,"Modificado correctamente")#muestra un mensaje
                return HttpResponseRedirect(reverse('diverty:listado_reservas'))# lo redirige al listado de reservas
            else:
                data["form"]=formulario#en caso de que algo haya salido
    except Reservas.DoesNotExist:
        #muestra el siguiente mensaje si la reserva no existe
        messages.error(request,"La reserva "+str(id)+" No se encontro ")
        return HttpResponseRedirect(reverse('diverty:listado_reservas'))
    #renderiza el formulario con los datos del diccionario
    return render (request,'diverty/modificar_reservas.html',data)

def eliminarReservas(request,id):
    try:
        session=request.session.get("login",False)#rescata la session
        #si la session es de administrador o empleado entonces se podra eliminar una reserva
        if session and (session[2] ==1 or session[2] ==2):
            reservas=Reservas.objects.get(pk=id)#obtiene el id de la reserva a eliminar
            reservas.delete()#la elimina
            messages.success(request,"Eliminado correctamente")#envia un mensaje 
        else:
            #si la session es usuario entonces lo redirigie al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
    except Reservas.DoesNotExist:
        #mostrara el siguiente mensaje si la reserva no existe
        messages.error(request,"La reserva "+str(id)+"no se encontro")
    # redirigira al administrador o empleado al listado de las reservas si se elimino correctamente
    return HttpResponseRedirect(reverse('diverty:listado_reservas'))

def crud_aviso(request):
    session=request.session.get("login",False)#obtiene la session
    #si la session es del administrador o empleado entonces podra ver el listado de atracciones
    if session and (session[2] ==1 or session[2] ==2):
        registros_tablas=Aviso.objects.all()#se trae todos los registros de atracciones
        paginator=Paginator(registros_tablas,4)#va a mostrar por pagina 4  registros de atracciones
        page=request.GET.get('page') or 1#rescata el numero de paginas
        #sobreescribe registros_tablas pero con ello se traera todos los registros de cada pagina de atracciones
        registros_tablas=paginator.get_page(page)
        paginactual=int(page)#convierte el numero de paginas a int
        paginas=range(1,registros_tablas.paginator.num_pages+1)#permite incrementar a una pagina si pasa el limite que es de 4
        data={
            'registros_tablas':registros_tablas,
            'paginactual':paginactual,
            'paginas':paginas
    }
    else:
        return HttpResponseRedirect(reverse("diverty:index",args=()))# en caso de que la session sea de clientes lo redirigira al index
    return render (request,'diverty/crud_avisos.html',data)#renderiza el listado y se trae todos los datos de atracciones

def guardarAviso(request):
    session=request.session.get("login",False)#obtiene la session
    if session and (session[2] ==1 or session[2] ==2):# si la session es de administrador o empleado permite guardar una reserva
        data={
            "form":AvisoForm()#crea una instancia de reservas que es el formulario con todos los campos que necesita
    }
    else:
        return HttpResponseRedirect(reverse('diverty:index',args=()))# en caso de que la session sea de cliente lo redirige al index
    if request.method=='POST':
        formulario=AvisoForm(data=request.POST,files=request.FILES)#captura todos los datos introduccidos por el usuario
        if formulario.is_valid():# si el formulario es valido,entonces:
            formulario.save()#guarda el formulario
            messages.success(request,"Guardado correctamente ")#muestra el mensaje
            return HttpResponseRedirect(reverse('diverty:listar_aviso'))#lo redirige al listado de reservas
        else:
            # en caso de que algo haya salido mal,rellena el formulario con todos los datos erroneos que salieron
            data["form"]=formulario
    # renderiza el formulario de reservas y el data permite tanto mostrar los campos de dicho formulario como poder guardar con los datos que ingrese el usuario
    return render (request,'diverty/formulario_avisos.html',data)

def editarAviso(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # si la session es del administrador o empleado entonces podra editar una reserva
        if session and (session[2] ==1 or session[2] ==2):
            avisos=Aviso.objects.get(pk=id)#obtiene el id de la reserva 
            #crea un diccionario que contrenda los campos de dicho formulario que correspondan al id
            data={
                "form":AvisoForm(instance=avisos)
        }
        else:
            # en caso de que la session sea de usuario entonces lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST':
            #permite llenar el formulario con los datos que correspondan al id y permite modificar los datos
            formulario=AvisoForm(data=request.POST,instance=avisos,files=request.FILES)
            if formulario.is_valid():#si el formulario es valido,entonces
                formulario.save()#guardar el formulario
                messages.success(request,"Modificado correctamente")#muestra un mensaje
                return HttpResponseRedirect(reverse('diverty:listar_aviso'))# lo redirige al listado de reservas
            else:
                data["form"]=formulario#si el formulario no es valido,se rellenara y se mostrara con los datos mal ingresados
    except Aviso.DoesNotExist:
        #si no existe una reserva mostrara el siguiente mensaje
        messages.error(request,"El aviso "+str(id)+" No se encontro ")
        #retorna al listado del aviso
        return HttpResponseRedirect(reverse('diverty:listar_aviso'))
    #renderiza  el formulario del aviso con  el diccionario
    return render (request,'diverty/modificar_aviso.html',data)
def eliminarAviso(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        #si la session es administrador o empleado permitira eliminar un aviso
        if session and (session[2] ==1 or session[2] ==2):
            avisos=Aviso.objects.get(pk=id)#obtiene el id del aviso a eliminar
            avisos.delete()#se elimina
            messages.success(request,"Eliminado correctamente")#envia el siguiente mensaje
        else:
            #si la session es de cliente lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
    except Aviso.DoesNotExist:
        #muestra el siguiente mensaje si un aviso no existe
        messages.error(request,"El aviso "+str(id)+"no se encontro")
    #retorna al listado de aviso
    return HttpResponseRedirect(reverse('diverty:listar_aviso'))
def tienda(request):
    q=Boletas_producto.objects.all()
    contexto={"datos":q}
    return render (request,'diverty/tienda.html',contexto)

def agregarCarrito(request,id):
    if request.method=="GET":
        bolsa=request.session.get('bolsa',False)
        carrito=request.session.get('carrito',False)
        cant=request.GET["cantidad"]

        conteo=0
        if not bolsa:
            request.session["carrito"]=[{ "productos":id,"cantidad":cant}]
            conteo+=1
            request.session["bolsa"]=conteo
            print("No existe",request.session["carrito"],"cantidad :",request.session["bolsa"])
        else:
            conteo=bolsa
            encontrado=False

            # averiguar si existe en la variable de session
            for r in carrito:
                if r["productos"] == id:
                    print("Encontrado")
                    r["cantidad"]=int(r["cantidad"])+int(cant)
                    encontrado=True
                    break
            if not encontrado:
                #crear nuevo
                print("No encontrado, se crea de nuevo")
                carrito.append({ "productos":id, "cantidad":cant })
                conteo+=1
            request.session["carrito"]=carrito
            request.session["bolsa"]=conteo
            print("Existe agrego ",request.session["carrito"],"cantidad",request.session["bolsa"])
        return HttpResponse(conteo)
    else:
        return HttpResponseRedirect(reverse('diverty:index', args=()))

    

def verCarrito(request):

    carrito=request.session.get('carrito',False)
    if carrito:
        total=0
        for productos in carrito:
            q=Boletas_producto.objects.get(codigo_producto=productos["productos"])
            productos["nombre_boleta_producto"]=q.nombre_boleta_producto
            productos["precio"]=q.precio
            productos["foto"]=q.foto
            productos["descuento"]=q.descuento
            if q.descuento==None:
                productos["subtotal"]=int(productos["cantidad"])*q.precio
            else:

                productos["subtotal"]=int(productos["cantidad"])*q.precio-q.descuento.precio
            if productos["subtotal"]<0:
                productos["subtotal"]=int(productos["cantidad"])*q.precio*0
                total+=productos["subtotal"]
                contexto={"datos":carrito,"total":total}
            else:
                total+=productos["subtotal"]
                contexto={"datos":carrito,"total":total}
        return render (request,'diverty/carrito.html',contexto)
    else:
        return HttpResponseRedirect(reverse("diverty:index",args=()))


def quitarProducto(request,id):
    carrito=request.session.get("carrito",False)
    bolsa=request.session.get("bolsa",False)
    if carrito:
        for productos in carrito:
            if productos["productos"]==id:
                print("Encontrado y eliminado")
                carrito.remove(productos)
                bolsa-=1
                
            print("fin")
        request.session["carrito"] = carrito
        request.session["bolsa"] = bolsa
        return HttpResponseRedirect(reverse("diverty:carro",args=()))
    else:
        return HttpResponseRedirect(reverse("diverty:index",args=()))

def limpiarCarrito(request):
    try:
        del request.session["carrito"]
        del request.session["bolsa"]
        return HttpResponseRedirect(reverse("diverty:carro",args=()))
    except:
        return HttpResponseRedirect(reverse("diverty:carro",args=()))
    

def guardarPedido(request):
    session=request.session.get("login",False)
    if session:
        carrito=request.session.get("carrito",False)
        if carrito:
            usuario=Usuario.objects.get(pk=session[0])
            from datetime import datetime
            fecha_envio=datetime.now()
            direccionPedido=request.POST["dir"]
            estadoPedido='1'

            from django.db import transaction
            try:
                with transaction.atomic():
                    q=Pedido(cliente=usuario,fecha=fecha_envio,direccion_de_envio=direccionPedido,estado=estadoPedido)
                    q.save()
                    ultimo=Pedido.objects.latest('id')
                    print("Encabezado pedido",ultimo)

                    for productos in carrito:
                        pro=Boletas_producto.objects.get(codigo_producto=productos["productos"])
                        
                        #stock
                        if int(productos["cantidad"])<=pro.stock:
                            #guardado masivo a la base de datos

                            PedidoProducto.objects.create(pedido=ultimo,producto=pro,cantidad=int(productos["cantidad"]),precio=pro.precio)
                            #disminuir stock del producto
                            pro.stock-=int(productos["cantidad"])
                            pro.save()
                        else:

                            messages.error(request, "Cantidad de producto " + str(productos["productos"]) + " supera STOCK " + str(pro.stock))
                            raise Exception("stock")
                    # vaciar carrito
                    del request.session["carrito"]
                    del request.session["bolsa"]
                    messages.success(request,"Pedido guardado correctamente")
                    return HttpResponseRedirect(reverse("diverty:index",args=()))
            except:
                return HttpResponseRedirect(reverse("diverty:carro",args=()))
        else:
            return HttpResponseRedirect(reverse("diverty:index"),args=())
    else:
        messages.error(request,"Primero debe loguear para comprar ")
        return HttpResponseRedirect(reverse("diverty:formulario_login",args=()))


def editarCarrito(request,id,cantidad):
    carrito=request.session.get("carrito",False)
    if carrito:
        for productos in carrito:
            if productos["productos"] == id:
                print("Encontrado y actualizado")
                productos["cantidad"]=int(cantidad)
             
            print("fin")
        request.session["carrito"]=carrito
        return HttpResponse("Ok")
    else:
        return HttpResponse("No existe el carrito")


def crud_productos(request):

    session=request.session.get("login",False)
    if session and (session[2] ==1 or session[2] ==2):
        # obtiene los objetos de tipo de cliente
        registros_tablas=Boletas_producto.objects.all() 
        # crea una instancia de tipo paginator en donde  se le indica a que instancia quiere utilizar y cuantos registos por pagina
        paginator=Paginator(registros_tablas,4)
        # rescata el numero de paginas al interactuar el usuario con la paginacion
        page=request.GET.get('page') or 1
        # se sobreescribe la variable registros_tablas para que se obtengan todos los clientes que esten dentro de la variable page que a su vez contiene el numero de la pagina en que se encuentra ubicado el usuario 
        registros_tablas=paginator.get_page(page) 
        # permite que ese numero de pagina que se pasa como string mediante el get en la url del navegador se convierta a int con el proposito de hacer un for que vaya contando y imprimiendo el numero de paginas que se necesita y que en caso de que una pagina supere las 4 que vienen por defecto este se incremente en 1 nueva pagina
        paginactual=int(page)
        # permite hacer un contador desde el methodo range que permite ir desde el 1 que es la primer pagina hasta el numero de pagina en que se ubica el usuario + la siguiente esto con el fin de que el usuario pueda interactuar con la actual y siguiente página a la que le vaya a dar click.
        paginas=range(1,registros_tablas.paginator.num_pages+1)
        data={
            'registros_tablas':registros_tablas,
             #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginas':paginas,
            #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginactual':paginactual 
        }
    else:
        return HttpResponseRedirect(reverse('diverty:index'))
    # renderizado del html  con el diccionario pasado como parametro para listar los objetos de tipo cliente y implementar las funcionalidades del páginado
    return render (request,'diverty/crud_boletas.html',data) 

def guardarProductos(request):
    session=request.session.get("login",False)#obtiene la session
    if session and (session[2] ==1 or session[2] ==2):# si la session es de administrador o empleado permite guardar una reserva
        data={
            "form":Boletas_productoForm()#crea una instancia de reservas que es el formulario con todos los campos que necesita
    }
    else:
        return HttpResponseRedirect(reverse('diverty:index',args=()))# en caso de que la session sea de cliente lo redirige al index
    if request.method=='POST':
        formulario=Boletas_productoForm(data=request.POST,files=request.FILES)#captura todos los datos introduccidos por el usuario
        if formulario.is_valid():# si el formulario es valido,entonces:
            formulario.save()#guarda el formulario
            messages.success(request,"Guardado correctamente ")#muestra el mensaje
            return HttpResponseRedirect(reverse('diverty:listar_productos'))#lo redirige al listado de reservas
        else:
            # en caso de que algo haya salido mal,rellena el formulario con todos los datos erroneos que salieron
            data["form"]=formulario
    # renderiza el formulario de reservas y el data permite tanto mostrar los campos de dicho formulario como poder guardar con los datos que ingrese el usuario
    return render (request,'diverty/formulario_productos.html',data)

def editarProductos(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # si la session es del administrador o empleado entonces podra editar una reserva
        if session and (session[2] ==1 or session[2] ==2):
            productos=Boletas_producto.objects.get(pk=id)#obtiene el id de la reserva 
            #crea un diccionario que contrenda los campos de dicho formulario que correspondan al id
            data={
                "form":Boletas_productoForm(instance=productos)
        }
        else:
            # en caso de que la session sea de usuario entonces lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST':
            #permite llenar el formulario con los datos que correspondan al id y permite modificar los datos
            formulario=Boletas_productoForm(data=request.POST,instance=productos,files=request.FILES)
            if formulario.is_valid():#si el formulario es valido,entonces
                formulario.save()#guardar el formulario
                messages.success(request,"Modificado correctamente")#muestra un mensaje
                return HttpResponseRedirect(reverse('diverty:listar_productos'))# lo redirige al listado de reservas
            else:
                data["form"]=formulario#si el formulario no es valido,se rellenara y se mostrara con los datos mal ingresados
    except productos.DoesNotExist:
        #si no existe una reserva mostrara el siguiente mensaje
        messages.error(request,"El producto "+str(id)+" No se encontro ")
        #retorna al listado del aviso
        return HttpResponseRedirect(reverse('diverty:listar_productos'))
    #renderiza  el formulario del aviso con  el diccionario
    return render (request,'diverty/modificar_productos.html',data)

def eliminarProductos(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        #si la session es administrador o empleado permitira eliminar un aviso
        if session and (session[2] ==1 or session[2] ==2):
            productos=Boletas_producto.objects.get(pk=id)#obtiene el id del aviso a elimina
            carrito=request.session.get("carrito",False)
            bolsa=request.session.get("bolsa",False)
            del request.session["carrito"]
            del request.session["bolsa"]
            
            productos.delete()#se elimina
            messages.success(request,"Eliminado correctamente")#envia el siguiente mensaje
        else:
            #si la session es de cliente lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
    except IntegrityError:
        messages.error(request,"error,primero elimine los guardados del carrito para poder eliminar el producto")
    except productos.DoesNotExist:
        #muestra el siguiente mensaje si un aviso no existe
        messages.error(request,"El producto "+str(id)+"no se encontro")
    #retorna al listado de aviso
    return HttpResponseRedirect(reverse('diverty:listar_productos'))


def crud_pedidos(request):
    session=request.session.get("login",False)
    if session and (session[2] ==1 or session[2] ==2):
        # obtiene los objetos de tipo de cliente
        registros_tablas=Pedido.objects.all()
        # crea una instancia de tipo paginator en donde  se le indica a que instancia quiere utilizar y cuantos registos por pagina
        paginator=Paginator(registros_tablas,4)
        # rescata el numero de paginas al interactuar el usuario con la paginacion
        page=request.GET.get('page') or 1
        # se sobreescribe la variable registros_tablas para que se obtengan todos los clientes que esten dentro de la variable page que a su vez contiene el numero de la pagina en que se encuentra ubicado el usuario 
        registros_tablas=paginator.get_page(page) 
        # permite que ese numero de pagina que se pasa como string mediante el get en la url del navegador se convierta a int con el proposito de hacer un for que vaya contando y imprimiendo el numero de paginas que se necesita y que en caso de que una pagina supere las 4 que vienen por defecto este se incremente en 1 nueva pagina
        paginactual=int(page)
        # permite hacer un contador desde el methodo range que permite ir desde el 1 que es la primer pagina hasta el numero de pagina en que se ubica el usuario + la siguiente esto con el fin de que el usuario pueda interactuar con la actual y siguiente página a la que le vaya a dar click.
        paginas=range(1,registros_tablas.paginator.num_pages+1)
        data={
            'registros_tablas':registros_tablas,
             #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginas':paginas,
            #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginactual':paginactual 
        }
    else:
        return HttpResponseRedirect(reverse('diverty:index'))
    # renderizado del html  con el diccionario pasado como parametro para listar los objetos de tipo cliente y implementar las funcionalidades del páginado
    return render (request,'diverty/listado_pedidos.html',data)
def guardarPedidos(request):
    session=request.session.get("login",False)#obtiene la session
    if session and (session[2] ==1 or session[2] ==2):# si la session es de administrador o empleado permite guardar una reserva
        data={
            "form":PedidoForm()#crea una instancia de reservas que es el formulario con todos los campos que necesita
    }
    else:
        return HttpResponseRedirect(reverse('diverty:index',args=()))# en caso de que la session sea de cliente lo redirige al index
    if request.method=='POST':
        formulario=PedidoForm(data=request.POST)#captura todos los datos introduccidos por el usuario
        if formulario.is_valid():# si el formulario es valido,entonces:
            formulario.save()#guarda el formulario
            messages.success(request,"Guardado correctamente ")#muestra el mensaje
            return HttpResponseRedirect(reverse('diverty:listar_productos'))#lo redirige al listado de reservas
        else:
            # en caso de que algo haya salido mal,rellena el formulario con todos los datos erroneos que salieron
            data["form"]=formulario
    # renderiza el formulario de reservas y el data permite tanto mostrar los campos de dicho formulario como poder guardar con los datos que ingrese el usuario
    return render (request,'diverty/formulario_pedidos.html',data)



def editarPedidos(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        # si la session es del administrador o empleado entonces podra editar una reserva
        if session and (session[2] ==1 or session[2] ==2):
            pedidos=Pedido.objects.get(pk=id)#obtiene el id de la reserva 
            #crea un diccionario que contrenda los campos de dicho formulario que correspondan al id
            data={
                "form":PedidoForm(instance=pedidos)
        }
        else:
            # en caso de que la session sea de usuario entonces lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
        if request.method=='POST':
            #permite llenar el formulario con los datos que correspondan al id y permite modificar los datos
            formulario=PedidoForm(data=request.POST,instance=pedidos)
            if formulario.is_valid():#si el formulario es valido,entonces
                formulario.save()#guardar el formulario
                messages.success(request,"Modificado correctamente")#muestra un mensaje
                return HttpResponseRedirect(reverse('diverty:listar_pedidos'))# lo redirige al listado de reservas
            else:
                data["form"]=formulario#si el formulario no es valido,se rellenara y se mostrara con los datos mal ingresados
    except pedidos.DoesNotExist:
        #si no existe una reserva mostrara el siguiente mensaje
        messages.error(request,"El producto "+str(id)+" No se encontro ")
        #retorna al listado del aviso
        return HttpResponseRedirect(reverse('diverty:listar_pedidos'))
    #renderiza  el formulario del aviso con  el diccionario
    return render (request,'diverty/modificar_pedidos.html',data)

def eliminarPedidos(request,id):
        try:

            session=request.session.get("login",False)#obtiene la session
        #si la session es administrador o empleado permitira eliminar un aviso
            if session and (session[2] ==1 or session[2] ==2):
                productos=Pedido.objects.get(pk=id)#obtiene el id del aviso a eliminar
                productos.delete()#se elimina
                messages.success(request,"Eliminado correctamente")#envia el siguiente mensaje
            else:
            #si la session es de cliente lo redirigira al index
                return HttpResponseRedirect(reverse('diverty:index',args=()))
        except productos.DoesNotExist:

            #muestra el siguiente mensaje si un aviso no existe
            messages.error(request,"El pedido "+str(id)+"no se encontro")
        except IntegrityError:
            messages.error(request,"Primero elimine el registro de detalles ")
        #retorna al listado de aviso
        return HttpResponseRedirect(reverse('diverty:listar_pedidos'))
    
def crud_productos_pedido(request):
    session=request.session.get("login",False)
    if session and (session[2] ==1 or session[2] ==2):
       
        # obtiene los objetos de tipo de cliente
        registros_tablas=PedidoProducto.objects.all()
       
        # crea una instancia de tipo paginator en donde  se le indica a que instancia quiere utilizar y cuantos registos por pagina
        paginator=Paginator(registros_tablas,4)
        # rescata el numero de paginas al interactuar el usuario con la paginacion
        page=request.GET.get('page') or 1
        # se sobreescribe la variable registros_tablas para que se obtengan todos los clientes que esten dentro de la variable page que a su vez contiene el numero de la pagina en que se encuentra ubicado el usuario 
        registros_tablas=paginator.get_page(page) 
        # permite que ese numero de pagina que se pasa como string mediante el get en la url del navegador se convierta a int con el proposito de hacer un for que vaya contando y imprimiendo el numero de paginas que se necesita y que en caso de que una pagina supere las 4 que vienen por defecto este se incremente en 1 nueva pagina
        paginactual=int(page)
        # permite hacer un contador desde el methodo range que permite ir desde el 1 que es la primer pagina hasta el numero de pagina en que se ubica el usuario + la siguiente esto con el fin de que el usuario pueda interactuar con la actual y siguiente página a la que le vaya a dar click.
        paginas=range(1,registros_tablas.paginator.num_pages+1)
        data={
            'registros_tablas':registros_tablas,
             #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginas':paginas,
            #captura del dato por medio de un diccionario esto con el fin de pasarselo al html y que pueda implementar las funcionalidades correctamente
            'paginactual':paginactual 
        }
    else:
        return HttpResponseRedirect(reverse('diverty:index'))
    # renderizado del html  con el diccionario pasado como parametro para listar los objetos de tipo cliente y implementar las funcionalidades del páginado
    return render (request,'diverty/listado_productos_pedido.html',data) 
def eliminarDetalles(request,id):
    try:
        session=request.session.get("login",False)#obtiene la session
        #si la session es administrador o empleado permitira eliminar un aviso
        if session and (session[2] ==1 or session[2] ==2):
            productos=PedidoProducto.objects.get(pk=id)#obtiene el id del aviso a eliminar
            productos.delete()#se elimina
            messages.success(request,"Eliminado correctamente")#envia el siguiente mensaje
        else:
            #si la session es de cliente lo redirigira al index
            return HttpResponseRedirect(reverse('diverty:index',args=()))
    except productos.DoesNotExist:
        #muestra el siguiente mensaje si un aviso no existe
        messages.error(request,"El detalle "+str(id)+"no se encontro")
    #retorna al listado de aviso
    return HttpResponseRedirect(reverse('diverty:listar_productos_del_pedido'))
    


    

   







