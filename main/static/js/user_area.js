//--------------DOM--------------//
const default_pics = document.querySelectorAll('.default-inmueble-pic');
const tetrade_palette = ['#ffa500', '#3fc1b4', '#2e1377', '#12192C', '#4089ce'];

//--------DOM STYLING--------//
default_pics.forEach((pic)=>{
    pic.style.color = tetrade_palette[Math.floor(Math.random() * tetrade_palette.length)]
});

//---------SWIPPER JS-----------//
var swiper = new Swiper(".imgSwiper", {
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
});