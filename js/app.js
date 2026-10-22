const navMenu = document.getElementById("navMenu");
const menuToggle = document.getElementById("menuToggle");

const copyEmailButton = document.getElementById("copyEmailButton");
const emailText = document.getElementsByClassName("email__label")[0].textContent;
const copyText = document.querySelector("#copyEmailButton .copy-text");


// Función para alternar la visibilidad del menú de navegación
function toggleMenu() {
  navMenu.classList.toggle("show");
  menuToggle.setAttribute("aria-expanded", navMenu.classList.contains("show"));
};

// Evento para el botón de menú
menuToggle.addEventListener("click", toggleMenu);


// Cerrar el menú al hacer clic en un enlace
const menuLinks = document.querySelectorAll(".menu-item__content a");
menuLinks.forEach(link => {
  link.addEventListener("click", toggleMenu);
});

// Cerrar el menú con la tecla ESC
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && navMenu.classList.contains('show')) {
    menuToggle.setAttribute('aria-expanded', 'false');
    navMenu.classList.remove('show');
    menuToggle.focus();
  }
});

// Función para copiar el email al portapapeles
let copyFeedbackTimeoutId;
const copyEmail = () => {
  navigator.clipboard.writeText(emailText).then(() => {
    clearTimeout(copyFeedbackTimeoutId);

    copyText.textContent = '¡Copiado!';

    copyFeedbackTimeoutId = setTimeout(() => {
      copyText.textContent = 'Copiar';
    }, 2000);

    console.log('Email copiado al portapapeles: ', emailText);
  }).catch(err => {
    console.error('Error al copiar el email: ', err);
  });
}

// Evento para el botón de copiar email
copyEmailButton.addEventListener('click', () => {
  copyEmail();
});


