const navMenu = document.getElementById("navMenu");
const menuToggle = document.getElementById("menuToggle");

let btn = document.getElementById("copyEmail");
let copy = document.getElementsByClassName("email__label")[0].textContent;


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

// Evento con la tecla esc
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && navMenu.classList.contains('show')) {
    menuToggle.setAttribute('aria-expanded', 'false');
    navMenu.classList.remove('show');
    menuToggle.focus();
  }
});

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



