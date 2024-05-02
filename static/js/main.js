
import {ponerMayusculas}  from './resources.js'

function validarContenido(campos) {
  let contenido = true

  var botonCerrar = document.getElementById('boton-cerrar');
  botonCerrar.style.display = 'block'; // Muestra el botón "Aceptar"

  let error = 'error'
  
  document.getElementById(error).innerHTML = '';

      try {
        let camposVacios = []
        campos.forEach(function(campo) {
          let valor = document.getElementById(campo).value;
          if (valor === '') {
            // console.log(campo)
            camposVacios.push(campo)
            contenido = false
          }
        })
  
        if (contenido === false){
          let errorCampos = "Debe de llenar los campos:"
          
          camposVacios.forEach(function(campo) {
            let campoClean = campo
            if (campo.includes('_')) {
              campoClean = campo.replace(/_/g, ' ');
            } else {              
              let formatError = `${errorCampos} <br> ${ponerMayusculas(campo)}`;
              errorCampos = formatError
            }
          })
          console.log(errorCampos)
          document.getElementById(error).innerHTML = errorCampos

        }
      }
      catch(error){
        console.error(error)
      }

      return contenido; 
}
function probarFuncion(){
  console.log("Si se esta ejecutando el HTML 1")
  return false
}

function aceptar(modulo){
  document.getElementById(modulo).innerHTML = '';
}
window.validarContenido = validarContenido;
window.aceptar = aceptar;

function ocultarError() {
  document.getElementById('error').style.display = 'none'; // Oculta el mensaje
      var botonCerrar = document.getElementById('boton-cerrar');
    botonCerrar.style.display = 'none'; // Oculta el botón "Aceptar"

}

// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    var botonCerrar = document.getElementById('boton-cerrar');
    botonCerrar.addEventListener('click', ocultarError);
});