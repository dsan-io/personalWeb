let btn = document.getElementById("copyEmail");
let copy = document.getElementsByClassName("email__label")[0].textContent;
// let copyMessage = document.getElementById("copyMessage");

// Función 
const copyEmail = () => {
  navigator.clipboard.writeText(copy).then(() => {
    console.log('Email copiado al portapapeles: ', copy);
    // copyMessage.style.display = "block"; // Mostrar el mensaje
    // setTimeout(() => {
    //   copyMessage.style.display = "none"; // Ocultar el mensaje después de 2 segundos
    // }, 2000);
  }).catch(err => {
    console.error('Error al copiar el email: ', err);
  });
}

// Evento
btn.addEventListener('click', () => {
  copyEmail();
});



