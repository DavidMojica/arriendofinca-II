//Forms
const formAccount = document.getElementById('formAccount');
const formUsername = document.getElementById('formUsername');
const formPass = document.getElementById('formPass');

//Campos unitarios
const nombre = document.getElementById('edit_nombre');
const apellidos = document.getElementById('edit_apellidos');
const email = document.getElementById('edit_email');
const celular = document.getElementById('edit_celular');

const username = document.getElementById('username');

const edit_password_old = document.getElementById('edit_password_old');
const edit_password_1 = document.getElementById('edit_password_1');
const edit_password_2 = document.getElementById('edit_password_2');

//variables
const nombreMinLength = 2;
const apellidosMinLength = 3;
const celularNumberChars = 10;
const passwordMinLegth = 8;
const usernameMinLength = 4;

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

let validationResult = undefined;
let badgeChild = undefined;

//-------------------------------------------------//
//-----------Validaciones formulario 1-------------//
//-------------------------------------------------//

formAccount.addEventListener('submit', e => {
    e.preventDefault();
    validationResult = formAccountValidations();
    if (validationResult !== '0') createToastNotify(1,'Error en información básica',  validationResult);
    else formAccount.submit();
});

const formAccountValidations = () =>{
    if (nombre.value.trim().length < nombreMinLength) return "Nombre demasiado corto.";
    if (apellidos.value.trim().length < apellidosMinLength) return "Apellidos demasiado cortos.";
    if (celular.value.trim().length != celularNumberChars) return "El número de celular no tiene 10 dígitos.";
    if (!emailRegex.test(email.value.trim())) return "Ingrese un correo electrónico válido.";
    return '0';
}

//-------------------------------------------------//
//-----------Validaciones formulario 2-------------//
//-------------------------------------------------//
formUsername.addEventListener('submit', e=>{
    e.preventDefault();
    validationResult = formUsernameValidations();
    if (validationResult !== '0') createToastNotify(1, 'Error en Nombre de usuario', validationResult);
    else formUsername.submit();
});

const formUsernameValidations = () =>{
    if (username.value.trim().length < usernameMinLength) return "El nombre de usuario es demasiado corto. Se necesitan 4 carácteres como mínimo.";
    return '0';
}

//-------------------------------------------------//
//-----------Validaciones formulario 3-------------//
//-------------------------------------------------//

formPass.addEventListener('submit', e=>{
    e.preventDefault();
    validationResult = formPassValidations();
    if(validationResult !== '0') createToastNotify(1, 'Error zona de contraseñas', validationResult);
    else formPass.submit();
});

const formPassValidations = () =>{
    if (edit_password_old.value.length < passwordMinLegth) return "La contraseña anterior es demasiado corta";
    if (edit_password_1.value.length < passwordMinLegth) return "La contraseña nueva es demasiado corta";
    if (edit_password_1.value.length < passwordMinLegth) return "Confirmar contraseña es demasiado corta";
    if (edit_password_1.value !== edit_password_2.value) return "Las contraseñas no coinciden";

    return '0';
}
//-------------------------------------------------//
//--------------Interacción con el DOM-------------//
//-------------------------------------------------//
const changeBadgeColor = (type, badge) => {
    if (type == 0) {
        badge.classList.remove('bg-danger');
        badge.classList.add('bg-success');
    } else if(type == 1) {
        badge.classList.remove('bg-success');
        badge.classList.add('bg-danger');
    }
}

//------------FORMULARIO 1-------------//
nombre.addEventListener('input',(e)=>{
    const spanBadge = e.target.parentElement.querySelector('.badge');
    if (e.target.value.trim().length >= nombreMinLength) changeBadgeColor(0, spanBadge);
    else changeBadgeColor(1, spanBadge);
});

apellidos.addEventListener('input',(e)=>{
    const spanBadge = e.target.parentElement.querySelector('.badge');
    if (e.target.value.trim().length >= apellidosMinLength) changeBadgeColor(0, spanBadge);
    else changeBadgeColor(1, spanBadge);
});

email.addEventListener('input', (e)=>{
    const spanBadge = e.target.parentElement.querySelector('.badge');
    if(emailRegex.test(email.value)) changeBadgeColor(0, spanBadge);
    else changeBadgeColor(1, spanBadge);
});

celular.addEventListener('input',(e)=>{
    const spanBadge = e.target.parentElement.querySelector('.badge');
    if (e.target.value.trim().length === celularNumberChars) changeBadgeColor(0, spanBadge);
    else changeBadgeColor(1, spanBadge);
});

//------------FORMULARIO 2-------------//
username.addEventListener('input',(e)=>{
    const spanBadge = e.target.parentElement.querySelector('.badge');
    if (e.target.value.trim().length >=usernameMinLength) changeBadgeColor(0, spanBadge);
    else changeBadgeColor(1, spanBadge);
});

//------------FORMULARIO 3-------------//
edit_password_old.addEventListener('input',(e)=>{
    const spanBadge = e.target.parentElement.querySelector('.badge');
    if (e.target.value.trim().length >= passwordMinLegth) changeBadgeColor(0, spanBadge);
    else changeBadgeColor(1, spanBadge);
});

edit_password_1.addEventListener('input',(e)=>{
    const spanBadge = e.target.parentElement.querySelector('.badge');
    badgeChild = edit_password_1.parentElement.querySelector('.badge');
    if (e.target.value.trim().length >= passwordMinLegth && (edit_password_1.value === edit_password_2.value)){
        changeBadgeColor(0, spanBadge);
        badgeChild = edit_password_2.parentElement.querySelector('.badge');
        changeBadgeColor(0,badgeChild);
    }
    else{
        changeBadgeColor(1, spanBadge);
        changeBadgeColor(1,badgeChild);
    }
});

edit_password_2.addEventListener('input',(e)=>{
    const spanBadge = e.target.parentElement.querySelector('.badge');
    badgeChild = edit_password_1.parentElement.querySelector('.badge');
    if (e.target.value.trim().length >= passwordMinLegth && (edit_password_1.value === edit_password_2.value)){
        changeBadgeColor(0, spanBadge);
        changeBadgeColor(0,badgeChild);
    }
    else {
        changeBadgeColor(1, spanBadge);
        changeBadgeColor(1,badgeChild);
    }
});

//-------------------------------------------------//
//---------------Inicialización DOM----------------//
//-------------------------------------------------//
//------------FORMULARIO 1-------------//
badgeChild = nombre.parentElement.querySelector('.badge');
if (nombre.value.trim().length >= nombreMinLength) changeBadgeColor(0, badgeChild);

badgeChild = apellidos.parentElement.querySelector('.badge');
if (apellidos.value.trim().length >= apellidosMinLength) changeBadgeColor(0, badgeChild);

badgeChild = email.parentElement.querySelector('.badge');
if (emailRegex.test(email.value)) changeBadgeColor(0, badgeChild);

badgeChild = celular.parentElement.querySelector('.badge');
if (celular.value.trim().length === celularNumberChars) changeBadgeColor(0, badgeChild);

//------------FORMULARIO 2-------------//
badgeChild = username.parentElement.querySelector('.badge');
if (username.value.trim().length >= usernameMinLength) changeBadgeColor(0,badgeChild);
