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

        let x = document.getElementById("x");
        x.style.setProperty("display", "inline", "important");

        let form = document.getElementById('form');

        let valoresOriginales = {};
        form.querySelectorAll('input').forEach(input => {
          valoresOriginales[input.id] = input.value;
        });

        document.getElementById("datosOriginales").value = JSON.stringify(valoresOriginales);
        console.log(`Valores originales guardados: ${JSON.stringify(valoresOriginales)}`);
    
      }  

    if (button == 'xe'){

        
    }    
    
    if (button == 'guardar'){

    }    
    
    if (button == 'actualizar'){

    }

  return true;  // Esto permite que el formulario se envíe

}
function recargarPagina(ruta) {
  window.location.href = `/${ruta}`;  
}
// function filtrarCitas() {
//   const searchInput = document.getElementById('searchInput');
//   const citasBody = document.getElementById('citasBody');
//   const noResults = document.getElementById('noResults');

//   const busqueda = searchInput.value.toLowerCase();
//   const filas = citasBody.getElementsByTagName('tr');
//   let resultadosEncontrados = false;

//   for (let fila of filas) {
//       const doctor = fila.getElementsByTagName('td')[1].textContent.toLowerCase();
//       if (doctor.includes(busqueda)) {
//           fila.classList.remove('hidden');
//           resultadosEncontrados = true;
//       } else {
//           fila.classList.add('hidden');
//       }
//   }

//   noResults.classList.toggle('hidden', resultadosEncontrados);
// }
// searchInput.addEventListener('input', filtrarCitas);

window.validarContenido = validarContenido;
window.ocultarError = ocultarError;
window.logicaBotones = logicaBotones;
window.recargarPagina = recargarPagina;
window.filtrarCitas = filtrarCitas;