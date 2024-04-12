import { createToastNotify } from "./modules/ToastNotify";
import { changeBadgeColor } from "./modules/essentials";

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
    return '0';
});

const formPassValidations = () =>{
    if (oldPassword.value.length < passwordMinLegth) return "La contraseña anterior es demasiado corta";
    if (password.value.length < passwordMinLegth) return "La contraseña nueva es demasiado corta";
    if (password1.value.length < passwordMinLegth) return "Confirmar contraseña es demasiado corta";
    if (password.value !== password1.value) return "Las contraseñas no coinciden";

    return '0';
}