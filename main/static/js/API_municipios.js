//----------DOMINIO---------//
const domain = "http://127.0.0.1:8000/";
//-----VISTA OBJETIVO-----//
const view = "municipios_por_departamento";

//-----------DOM--------//
const departamento_select = document.getElementById('departamento-select');
const municipio_select = document.getElementById('municipio_select');
const form_crear = document.getElementById('form-crear');

// form_crear.addEventListener('submit', e=>{
//     e.preventDefault();
//     municipio_select.value = parseInt(municipio_select.value);
//     form_crear.submit();
// });

departamento_select.addEventListener('change',async function(){
    let departamento_id = departamento_select.value;
    try{
        const response = await fetch(`${domain}${view}?departamento_id=${departamento_id}`);
        const data = await response.json();
        municipio_select.innerHTML = '';
        data.forEach(municipio => {
            console.log(municipio);
            let option = document.createElement('option');
            option.value = municipio.id;
            option.text = municipio.description;
            municipio_select.appendChild(option);
        });
    } catch (error) {
        createToastNotify(1,"Error obteniendo municipios", error);
    }
});