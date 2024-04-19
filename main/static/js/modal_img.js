const images=[...document.querySelectorAll('.image')];
const popup = document.querySelector('.popup');
const closeBtn = document.querySelector('.close-btn');
const imageName = document.querySelector('.image-name');
const largeImage = document.querySelector('.large-image');
let index = 0;
images.forEach((item) =>{
    item.addEventListener('click', ()=>{
        largeImage.src = item.src;
        popup.classList.add('active');
    });
});

popup.addEventListener('click', ()=>{
    popup.classList.remove('active');
});

closeBtn.addEventListener('click', ()=>{
    popup.classList.remove('active');
})