// import * as resources  from './resources.js'
import ponerMayusculas from './resources.js';
// import { ponerMayusculas } from './resources.js';

function probarFuncion(){
    console.log("Si se esta ejecutando el HTML 1")
    return false
  }
let textoEnMinusculas = "esto debería estar en mayúsculas";
let textoEnMayusculas = ponerMayusculas(textoEnMinusculas);
console.log(textoEnMayusculas);  // Salida esperada: "Esto Debería Estar En Mayúsculas"
  export { probarFuncion };


//Verifica el tipo de módulo: Asegúrate de que no haya una mezcla de tipos de módulos (CommonJS y ES6) que pueda estar causando el problema.