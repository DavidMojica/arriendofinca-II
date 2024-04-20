//-------------DOM-------------//
const form_crear = document.getElementById('form-crear');
const precio = document.getElementById('precio');
const direccion = document.getElementById('direccion');
const area_construida = document.getElementById('area_construida');
const area = document.getElementById('area');
const habitaciones = document.getElementById('habitaciones');
const banios = document.getElementById('banios');
const imagenes = document.getElementById('imagenes');
const arriendo_venta = document.getElementById('arriendo_venta');
const tipo_cobro = document.getElementById('tipo_cobro');

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
    // validationResult = form_validators();
    // if (validationResult != "0") createToastNotify(1, "Error en detalles del inmueble", validationResult);
    // else 
    form_crear.submit();
});
//----------Validacion de imagenes---------//
imagenes.addEventListener('change', e=>{
    let files = e.target.files;

    validationResult = img_validators(files);
    if (validationResult !== "0"){
        createToastNotify(1, "Error en imágenes", validationResult);
        imagenes.value = '';
    }
    else createToastNotify(0, "Operación exitosa", "Las imagenes fueron cargadas correctamente.")
});

const img_validators = files =>{
    const img_maxMB_size = 2;
    //-----Cantidad de imágenes------//
    if (files.length > 5) return "Sólo se permiten un máximo de 5 imágenes.";
    
    //--------Peso de cada imagen--------//
    for (let i = 0; i < files.length; i++){
        let fileSizeInMB = files[i].size / (1024*1024);
        if (fileSizeInMB > img_maxMB_size) return "El tamaño máximo para cada imagen es de 2MB";
        //-------Tipo de archivo-------//
        const file = files[i];
        const fileType = file.type;

        // Validar el tipo de archivo
        if (!fileType.startsWith('image/')) {
            return 'El archivo "' + file.name + '" no es una imagen válida.';
        }
    }
    return "0";
}

//------------Validacion de periodo de cobro y tipo de transaccion---------//
arriendo_venta.addEventListener('change', e=>{
    if (e.target.value == 1){
        tipo_cobro.value = 5;
        tipo_cobro.disabled = true;

        for (let i = 0; i < tipo_cobro.options.length; i++) {
            if (tipo_cobro.options[i].value == 5) {
                tipo_cobro.options[i].selected = true;
                break;
            }
        }
    }
    else tipo_cobro.disabled = false;
});


const form_validators = () =>{
    //--Precio--//
    if (precio.value.trim().length < precio_validators.min_length || precio.value.trim().length >= precio_validators.max_length || isNaN(precio.value.trim())) return "El precio debe de ser superior a $100";
    //--Direccion--//
    if (direccion.value.trim().length < direccion_validators.min_length || direccion.value.trim().length >= direccion_validators.max_length) return "Longitud de dirección inválida";
    //--Area--//
    if (area.value.trim().length < area_validators.min_length || area.value.trim().length >= area_validators.max_length || isNaN(area.value.trim())) return "El area debe de estar entre 1mt y 9.999.999 de mts.";
    //--Area construida--//
    if (area_construida.value.trim().length < area_validators.min_length || area_construida.value.trim().length >= area_validators.max_length || isNaN(area_construida.value.trim())) return "El area debe de estar entre 1mt y 9.999.999 de mts.";
    //--Area construida 2--//
    if (parseFloat(area_construida.value) > parseFloat(area.value)) return "Error, el área construida no puede ser mayor al área del inmueble";
    //--Habitaciones--//
    if (habitaciones.value.trim().length < habitaciones_validators.min_length || habitaciones.value.trim().length >= habitaciones_validators.max_length || isNaN(habitaciones.value.trim())) return "Las habitaciones deben de estar entre 0 y 999";
    //--Baños--//
    if (banios.value.trim().length < banios_validators.min_length || banios.value.trim().length >= banios_validators.max_length || isNaN(banios.value.trim())) return "Los baños deben de estar entre 0 y 999";
    //---Imgs---//
    validationResult = img_validators(imagenes.files);
    if (validationResult !== "0") return validationResult;

    return "0";
}