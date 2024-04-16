//-------------DOM-------------//
const form_crear = document.getElementById('form-crear');
const precio = document.getElementById('precio');
const direccion = document.getElementById('direccion');
const area_construida = document.getElementById('area_construida');
const area = document.getElementById('area');
const habitaciones = document.getElementById('habitaciones');
const banios = document.getElementById('banios');

//------------VARIABLES----------//
const precio_validators = {'min_length': 2, 'max_length':20};
const direccion_validators = {'min_length': 2, 'max_length': 80}; 
const area_validators = {'min_length': 1, 'max_length': 7};
const habitaciones_validators = {'min_length': 1, 'max_length': 3};
const banios_validators = {'min_length': 1, 'max_length': 3};

let validationResult = undefined;
//------Events-----//
form_crear.addEventListener('submit', e=>{
    e.preventDefault();
    validationResult = form_validators();
    if (validationResult != "0") createToastNotify(1, "Error creando inmueble", validationResult);
    else form_crear.submit();
});

const form_validators = () =>{
    console.log(parseFloat(area_construida.value) > parseFloat(area.value));
    if (precio.value.trim().length < precio_validators.min_length || precio.value.trim().length >= precio_validators.max_length || isNaN(precio.value.trim())) return "El precio debe de ser superior a $100";
    if (direccion.value.trim().length < direccion_validators.min_length || direccion.value.trim().length >= direccion_validators.max_length) return "Longitud de dirección inválida";
    if (area.value.trim().length < area_validators.min_length || area.value.trim().length >= area_validators.max_length || isNaN(area.value.trim())) return "El area debe de estar entre 1mt y 9.999.999 de mts.";
    if (area_construida.value.trim().length < area_validators.min_length || area_construida.value.trim().length >= area_validators.max_length || isNaN(area_construida.value.trim())) return "El area debe de estar entre 1mt y 9.999.999 de mts.";
    if (parseFloat(area_construida.value) > parseFloat(area.value)) return "Error, el área construida no puede ser mayor al área del inmueble";
    if (habitaciones.value.trim().length < habitaciones_validators.min_length || habitaciones.value.trim().length >= habitaciones_validators.max_length || isNaN(habitaciones.value.trim())) return "Las habitaciones deben de estar entre 0 y 999";
    if (banios.value.trim().length < banios_validators.min_length || banios.value.trim().length >= banios_validators.max_length || isNaN(banios.value.trim())) return "Los baños deben de estar entre 0 y 999";

    return "0";
}