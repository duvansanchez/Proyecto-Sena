

{/* <search-and-results-form></search-and-results-form> */}
{/* <script>
// Este script solo se ejecuta después de que el DOM y los componentes se hayan cargado
document.addEventListener('DOMContentLoaded', () => {
    const results = {{ results | tojson }};
    console.log("Datos inyectados desde el backend:", results);

    const componente = document.querySelector('search-and-results-form');
    
    if (componente) {
        componente.results = results;
        console.log("Asignación completada");
    } else {
        console.error('El componente no se encontró en el DOM.');
    }
});
</script> */}



class SearchAndResultsForm extends HTMLElement {
    constructor() {
        super();

        // Crear el Shadow DOM y adjuntarlo al componente
        const shadow = this.attachShadow({ mode: 'open' });

        // Crear el estilo dentro del Shadow DOM
        const style = document.createElement('style');
        style.textContent = `
            *{
                padding: 0px;
                margin: 0px;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
                font-weight: 700;
            }
            body{
                display: flex;
                flex-direction: column;
                background: rgb(207,226,255);
                background: radial-gradient(circle, rgba(207,226,255,1) 15%, rgba(255,255,255,1) 100%);
            }
            .box{
                background-color: rgb(255, 255, 255);
                width: 500px;
                border: 3px solid rgb(0, 183, 255);
                margin: 0 auto;
                justify-content: center;
                text-align: center; 
            }
            .title{
                color: #26bddb;
            }
            .content-box {
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .content-result ul {
                list-style-type: none;
                padding: 0;
            }
            .content-result li {
                margin-bottom: 10px;
            }
            button {
                background-color: #26bddb;
                color: white;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                border-radius: 5px;
            }
        `;

        // Crear la estructura HTML dentro del Shadow DOM
        const wrapper = document.createElement('div');
        wrapper.innerHTML = `
            <div class="box">
                <div class="content-box">
                    <h3 class="title">Resultados</h3>
                </div>
                <div class="content-result">
                    <ul id="results-list">

                    </ul>
                </div>
            </div>
       `;

        // Adjuntar el estilo y el contenido al Shadow DOM
        shadow.appendChild(style);
        shadow.appendChild(wrapper);
    }

    // Método para renderizar los resultados
    set results(data) {

        //Obtener div content
        const resultsList = this.shadowRoot.getElementById('results-list');
        
        // Limpiar cualquier contenido previo
        resultsList.innerHTML = '';  
        console.log("Datos recibidos en results:", data);  // Verifica que el setter se ejecuta

        //Verificar si el componente trae resultados
        if (data && data.length > 0) {

            //Leer data
            data.forEach(res => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <input type="text" name="selected_results" value="${res}" style="color: red;">
                    <span>${res}</span>
                `;
                resultsList.appendChild(li);
            });
        } else {
            resultsList.innerHTML = '<li>No se encontraron resultados.</li>';
        }
    }
}

// Registrar el nuevo componente personalizado
customElements.define('search-and-results-form', SearchAndResultsForm);
