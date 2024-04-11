const wrapper = document.querySelector('.wrapper');
const registerLink = document.querySelector('.register-link');
const loginLink = document.querySelector('.login-link');
const registerForm = document.querySelector('#form-register');
const wrapperFormRegister = document.querySelector('.wrapper .form-box.register');

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

//311 311 0647