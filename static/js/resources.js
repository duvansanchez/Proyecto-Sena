function ponerMayusculas(cadena) {
    return cadena.toLowerCase().replace(/(^|\s)\S/g, function(letra) {
        return letra.toUpperCase();
    });
}
// function vaciarCampo(campo){
//     document.getElementById(campo).innerHTML = '';
// }
export { ponerMayusculas };
