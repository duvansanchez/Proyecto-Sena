function ponerMayusculas(cadena) {
    return cadena.toLowerCase().replace(/(^|\s)\S/g, function(letra) {
        return letra.toUpperCase();
    });
}
<<<<<<< HEAD
function vaciarCampo(campo){
    document.getElementById(campo).innerHTML = '';
}
export { ponerMayusculas,vaciarCampo };
=======
function aceptar(modulo){
    document.getElementById(modulo).innerHTML = '';
}
export { ponerMayusculas,aceptar };
>>>>>>> ef6d8354ad990c63b9552f7dfd9729d9aae3df5b
