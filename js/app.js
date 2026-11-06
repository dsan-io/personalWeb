const navMenu = document.getElementById("navMenu");
const menuToggle = document.getElementById("menuToggle");

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


// Copy email to clipboard

const copyEmailButton = document.getElementById("copyEmailButton");
const emailText =
  document.getElementsByClassName("email__label")[0].textContent;
const copyText = document.querySelector("#copyEmailButton .copy-text");

const copyDefault = "Copiar";

const copySuccess = "¡Copiado!";

const copyError = "Selecciónalo";

const copyFeedbackTimeout = 2000;

let copyFeedbackTimeoutId;

const messageStatus = function (message) {
  clearTimeout(copyFeedbackTimeoutId);
  copyText.textContent = message;
  copyFeedbackTimeoutId = setTimeout(() => {
    copyText.textContent = copyDefault;
  }, copyFeedbackTimeout);

}

const copyEmail = async () => {

  try {
    if (!navigator.clipboard) {
      throw new Error("Clipboard API no disponible");
    }
    await navigator.clipboard.writeText(emailText)
    messageStatus(copySuccess);

  } catch (error) {
    messageStatus(copyError);
    console.error("Error al acceder al portapapeles: ", error);
  }
};



copyEmailButton.addEventListener("click", copyEmail);
