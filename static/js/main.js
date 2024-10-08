import { ponerMayusculas } from "./resources.js";

let valoresOriginales = {};

function validarContenido(campos) {
  try{
    let enviarContenido = true;
    let mensajeError = document.getElementById("error");
    let botonCerrar = document.getElementById("boton-cerrar");
    
    console.log("Probando validacion")

    try {
      let camposVacios = [];
      
      campos.forEach(function (campo) {
        let valor = document.getElementById(campo).value;
        if (valor === "") {
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
        mensajeError.innerHTML = errorCampos;
        mensajeError.style.display = "block"; 
        botonCerrar.style.display = "block"; 
      }
      return enviarContenido;
    } catch (error) {
        alert(error);
    }
  }catch (error) {
    alert(error);
  }
}
function ocultarError() {
  document.getElementById("error").style.display = "none"; 
  let botonCerrar = document.getElementById("boton-cerrar");
  botonCerrar.style.display = "none"; 
  return false
}
function logicaBotones(button){
    console.log(`button en accion ${button}`)
    
    if (button == 'nuevo'){
        let buscar = document.getElementById("buscar");
        buscar.style.display = "none";
        let nuevo = document.getElementById("nuevo");
        nuevo.style.display = "none";
        let guardar = document.getElementById("guardar");
        guardar.style.setProperty("display", "inline", "important");
    }

    if (button == 'buscar'){
   
    }  

    if (button == 'editar'){
        let editar = document.getElementById("editar");
        editar.style.display = "none";

        
        let actualizar = document.getElementById("actualizar");
        actualizar.style.setProperty("display", "inline", "important");

        let x = document.getElementById("xe");
        x.style.setProperty("display", "inline", "important");

        valoresOriginales = {
          usuario: document.getElementById("usuario").value,
          cedula: document.getElementById("cedula").value,
          telefono: document.getElementById("telefono").value,
          correo: document.getElementById("correo").value,
          contrasena: document.getElementById("contraseña").value
        };
        document.getElementById("datosOriginales").value = JSON.stringify(valoresOriginales);
        console.log(`Valores originales guardados: ${JSON.stringify(valoresOriginales)}`);
    
      }  

    if (button == 'xe'){

        
    }    
    
    if (button == 'guardar'){

    }    
    
    if (button == 'actualizar'){
        valoresModificados = {
          usuario: document.getElementById("usuario").value,
          cedula: document.getElementById("cedula").value,
          telefono: document.getElementById("telefono").value,
          correo: document.getElementById("correo").value,
          contrasena: document.getElementById("contraseña").value
        };
        console.log(`Valores modificados: ${JSON.stringify(valoresModificados)}`);
    }

  return true;  // Esto permite que el formulario se envíe

}
function recargarPagina() {
  // Redirigir al endpoint original (ruta) como si fuera una nueva carga desde el servidor
  window.location.href = '/usuario';  // Cambia '/usuario' por la ruta de tu página
}


// window.addEventListener('beforeunload', function () {
//   // Redirigir al endpoint inicial cada vez que se intente recargar la página
//   console.log("recargando datos")
//   window.location.href = '/usuario';  // Esto garantiza que la página cargue desde el servidor
// });

window.validarContenido = validarContenido;
window.ocultarError = ocultarError;
window.logicaBotones = logicaBotones;
window.recargarPagina = recargarPagina;