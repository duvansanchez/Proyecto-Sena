import { ponerMayusculas, vaciarCampo } from "./resources.js";


function validarContenido(campos) {
  let enviarContenido = true;
  let botonCerrar = document.getElementById("boton-cerrar");
  let error = "error";
  
  vaciarCampo(error);
  
  try {
    let camposVacios = [];
    
    campos.forEach(function (campo) {
      let valor = document.getElementById(campo).value;
      if (valor === "") {
        //Agregar a lista de campos vacios y evitar el envio del contenido
        camposVacios.push(campo);
        enviarContenido = false;
      }
    });
    
    if (enviarContenido === false) {
      let errorCampos = "Debe de llenar los campos:";
      
      camposVacios.forEach(function (campo) {    
          let campoClean = campo    
          
          if (campo.includes("_")) {
            campoClean = campo.replace(/_/g, " ");
          }

          let formatError = `${errorCampos} <br> ${ponerMayusculas(campoClean)}`;
          errorCampos = formatError;
      });
      document.getElementById(error).innerHTML = errorCampos;
      botonCerrar.style.display = "block"; // Mostrar boton aceptar
    }
  } catch (error) {
    console.error(error);
  }

  return enviarContenido;
}

window.validarContenido = validarContenido;
window.ocultarError = ocultarError;

function ocultarError() {
  document.getElementById("error").style.display = "none"; 
  let botonCerrar = document.getElementById("boton-cerrar");
  botonCerrar.style.display = "none"; 
  return false
}

// ocultarError()
// Espera a que el DOM esté completamente cargado
// document.addEventListener("DOMContentLoaded", function () {
//   let botonCerrar = document.getElementById("boton-cerrar");
//   botonCerrar.addEventListener("click", ocultarError);
// });
