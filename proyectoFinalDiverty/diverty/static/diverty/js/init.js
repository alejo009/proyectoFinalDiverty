(function($){
  $(function(){

    $('.sidenav').sidenav();


  }); // end of document ready
})(jQuery); // end of jQuery name space Barra lateral,navegadores


$(document).ready(function(){
  $('.carousel').carousel();
  

  
}); // Carrusel de imagenes

//loader
document.addEventListener("DOMContentLoaded", function(){
	$('.preloader-background').delay(1700).fadeOut('slow');
	
	$('.preloader-wrapper')
		.delay(1700)
		.fadeOut();
    M.AutoInit();
});


