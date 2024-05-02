function ponerMayusculas(cadena) {
    return cadena.toLowerCase().replace(/(^|\s)\S/g, function(letra) {
        return letra.toUpperCase();
    });
}
function aceptar(modulo){
    document.getElementById(modulo).innerHTML = '';
}
export { ponerMayusculas,aceptar };
