//---Animation---//
const wrapper = document.querySelector('.wrapper');
const registerLink = document.querySelector('.register-link');
const loginLink = document.querySelector('.login-link');
const registerForm = document.querySelector('#form-register');
const wrapperFormRegister = document.querySelector('.wrapper .form-box.register');

//---Login---//
const LoginForm = document.getElementById('form-login');
const login_username = document.getElementById('username');
const login_password = document.getElementById('password');

const RegisterForm = document.getElementById('form-register');
const register_first_name = document.getElementById('new_nombre');
const register_last_name = document.getElementById('new_apellidos');
const register_documento = document.getElementById('new_documento');
const register_tipo_documento = document.getElementById('new_tipo_documento');
const register_username = document.getElementById('new_username');
const register_password = document.getElementById('new_password');
const register_celular = document.getElementById('new_celular');
const register_whatsapp = document.getElementById('new_whatsapp');
const register_email = document.getElementById('new_email');

//variables
const nombreMinLength = 2;
const apellidosMinLength = 3;
const documentoMinLength = 4;
const tipos_documento_maxid = 3;
const celularNumberChars = 10;
const passwordMinLegth = 8;
const usernameMinLength = 4;
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

let validationResult = undefined;
//----------------------------------------//
//---------------Animations---------------//
//----------------------------------------//
registerLink.addEventListener('click', ()=>{
    wrapper.classList.add('active');
    if (window.innerWidth < 768) wrapperFormRegister.style.width = "100%";
    setTimeout(()=>{
        registerForm.style.overflowX = 'hidden';
        registerForm.style.overflowY = 'auto';
    }, 2000);
});

loginLink.addEventListener('click', ()=>{
    wrapper.classList.remove('active','overflow-auto', 'overflow-x-hidden');
    registerForm.style.overflowX = 'hidden';
    registerForm.style.overflowY = 'hidden';
    if (window.innerWidth < 768){
        setTimeout(()=>{
            wrapperFormRegister.style.width = "0%";
        }, 2000);
    }
});

//----------------------------------------//
//--------------Validations---------------//
//----------------------------------------//
//--Login--//
LoginForm.addEventListener('submit', e=>{
    e.preventDefault();
    validationResult = LoginValidations();
    if (validationResult != '0') createToastNotify(1, "Error al iniciar sesión", validationResult);
    else LoginForm.submit();
});

const LoginValidations= () =>{
    if (login_username.value.length < usernameMinLength) return "Nombre de usuario demasiado corto";
    if (login_password.value.length < passwordMinLegth) return "Contraseña demasiado corta";
    return "0";
}
//--Register--//
RegisterForm.addEventListener('submit', e=>{
    e.preventDefault();
    validationResult = RegisterValidations();
    if (validationResult != '0') createToastNotify(1, "Error al registrarse", validationResult);
    else RegisterForm.submit();
});

const RegisterValidations = () =>{
    if (register_first_name.value.length < nombreMinLength) return "El nombre es demasiado corto";
    if (register_last_name.value.length < apellidosMinLength) return "Apellidos demasiado cortos";
    if (register_documento.value.length < documentoMinLength) return "Documento demasiado corto";
    if (isNaN(register_tipo_documento.value) || register_tipo_documento.value > tipos_documento_maxid) return "Por favor seleccione un tipo de documento válido";
    if (register_username.value.length < usernameMinLength) return "Nombre de usuario demasiado corto";
    if (register_password.value.length < passwordMinLegth) return "Contraseña demasiado corta";
    if (!emailRegex.test(register_email.value.trim())) return "Ingrese un correo electrónico válido.";
    if (register_celular.value.length != celularNumberChars) return "El número de celular no tiene 10 dígitos.";
    return '0';
}

