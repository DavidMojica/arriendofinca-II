const wrapper = document.querySelector('.wrapper');
const registerLink = document.querySelector('.register-link');
const loginLink = document.querySelector('.login-link');
const registerForm = document.querySelector('#form-register');

registerLink.addEventListener('click', ()=>{
    wrapper.classList.add('active');
    registerForm.style.overflowX = 'hidden';
    registerForm.style.overflowY = 'auto';

});

loginLink.addEventListener('click', ()=>{
    wrapper.classList.remove('active','overflow-auto', 'overflow-x-hidden');
    registerForm.style.overflowX = 'hidden';
    registerForm.style.overflowY = 'hidden';
});