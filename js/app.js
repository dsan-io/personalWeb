const navMenu = document.getElementById("navMenu");
const menuToggle = document.getElementById("menuToggle");

const copyEmailButton = document.getElementById("copyEmailButton");
const emailText =
  document.getElementsByClassName("email__label")[0].textContent;
const copyText = document.querySelector("#copyEmailButton .copy-text");


function toggleMenu() {
  navMenu.classList.toggle("show");
  menuToggle.setAttribute("aria-expanded", navMenu.classList.contains("show"));
  console.log(
    "Menú: ",
    navMenu.classList.contains("show") ? "visible" : "oculto",
  );
}

function closeMenu() {
  navMenu.classList.remove("show");
  menuToggle.setAttribute("aria-expanded", "false");
}


menuToggle.addEventListener("click", toggleMenu);


const menuLinks = document.querySelectorAll(".menu-item a");
menuLinks.forEach((link) => {
  link.addEventListener("click", closeMenu);
});


document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && navMenu.classList.contains("show")) {
    menuToggle.focus();
    closeMenu();
  }
});


let copyFeedbackTimeoutId;
const copyEmail = () => {
  navigator.clipboard
    .writeText(emailText)
    .then(() => {
      clearTimeout(copyFeedbackTimeoutId);

      copyText.textContent = "¡Copiado!";

      copyFeedbackTimeoutId = setTimeout(() => {
        copyText.textContent = "Copiar";
      }, 2000);

      console.log("Email copiado al portapapeles: ", emailText);
    })
    .catch((err) => {
      console.error("Error al copiar el email: ", err);
    });
};


copyEmailButton.addEventListener("click", () => {
  copyEmail();
});
