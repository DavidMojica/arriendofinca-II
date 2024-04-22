const precios = document.querySelectorAll('.precio');

precios.forEach(precio =>{
    let precio_text = precio.textContent;
    precio_text = precio_text.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    precio.textContent = precio_text;
});