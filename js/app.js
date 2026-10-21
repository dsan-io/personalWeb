let btn = document.getElementById("copyEmail");
let copy = document.getElementsByClassName("email__label")[0].textContent;

// Función 
const copyEmail = () => {
  navigator.clipboard.writeText(copy).then(() => {
    console.log('Email copiado al portapapeles: ', copy);
  }).catch(err => {
    console.error('Error al copiar el email: ', err);
  });
}

// Evento
btn.addEventListener('click', () => {
  copyEmail();
});



