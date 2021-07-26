
function validarPasswordRegistro() {
  nombre = $('#nombre_usuario').val()
  email = $('#email_usuario').val()
  p1 = $('#clave').val()
  p2 = $('#clave2').val()
  let $rol = $('nombreSelect');
  expresion = /\w+@\w+\.+[a-z]/;
  if (nombre == '' || email == '' || p1 == '' || p2 == '') {

    Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "Todos los campos son requeridos ",
    })
    return false;
  }
  else if (nombre.length > 30) {
    Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "El nombre es muy largo ",
    })
    return false;
  }
  else if (email.length > 50) {
    Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "El email es muy largo ",
    })
    return false;
  }
  else if (!expresion.test(email)) {
    Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "El correo no es valido ",
    })
    return false;
  }
  else if (p1.length < 8 || p1.lenght > 12) {
    Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "Ingrese una contraseña entre 8 y 12 digitos ",
    })
    return false;
  }
  else if (p1 !== p2) {
    Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "Las contraseñas no coinciden",
    })
    return false;
  }




}

function agregarCarrito(ruta, productos) {
  console.log("agregar producto: " + productos + ", al carrito de compras")
  cantidad = $('#' + productos).val()
  expresion = /^([0-9])*$/;
  console.log(cantidad)
  if (!expresion.test(cantidad) || (cantidad <= 0)) {
    Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "Se esperaba un valor superior ",
    })

    return false;

  }
  else {
    $.ajax({

      method: "GET",
      url: ruta,
      data: { "cantidad": cantidad },
      cache: false
    })
      .done(function (respuesta) {
        $("#carrito").html(respuesta);
      });
  }

}

function guardarPedido(event) {
  email = $('#direccion_envio').val()
  if (email === "") {
    event.preventDefault();
    return Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "Se esperaba un valor en la direccion ",
    });
  } else if (email.length < 15 || email.length > 20) {
    event.preventDefault();
    return Swal.fire({
      "icon": "error",
      "title": "Ops...",
      "text": "ingrese una direccion entre el rango desde 15 20 caracteres ",
    });
  }


  expresion = /^([0-9])*$/;

  $('.input-carrito').each(function () {
    if (this.value === "") {
      event.preventDefault();
      return Swal.fire({
        "icon": "error",
        "title": "Ops...",
        "text": "Se esperaba un valor ",
      });
    }
  });

  if (!confirm("Estas seguro?")) {
    event.preventDefault()
  }

}

const formatter = new Intl.NumberFormat('es-CO', {
  style: 'currency',
  currency: 'COP',
  minimumFractionDigits: 0
});
function editarCantidadCarrito(cantidad, productos, precio, campo_subtotal,ruta){
  console.log(cantidad+ " " + productos+ " " + precio+ " " + campo_subtotal+ " " + ruta)
  var subtotal = (cantidad * precio);

  $('#s_'+campo_subtotal).val(subtotal);
  
  subtotal = formatter.format(subtotal);

  $('#cambio_subtotal_'+productos).html(subtotal);
  
  // use type="text" with input to select the element
  subtotalesBotones = $("input:button");

  total = 0;
  for (var i=0; i< subtotalesBotones.length; i++){
    total = total +parseInt(subtotalesBotones[i].value);
  }
  total = formatter.format(total);
  $('#total_carrito').html(total);

  //llamado AJAX para actualizar variables de sesion, cantidad y producto
  rutaOriginal = ruta.split("/")
  ruta = "/"+rutaOriginal[1]+"/"+productos+"/"+cantidad+"/"
  console.log(ruta)
  $.ajax({
      method: "GET",
      url: ruta,
      cache: false
  })
  .done(function( respuesta ) {
      console.log( respuesta );
  });
}


 


