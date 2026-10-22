# 🌐 Portafolio Personal — Leonardo Sandoval

![App Screenshot](https://github.com/dsan-io/personalWeb/blob/main/assets/images/webPageDesktop.webp)
![App Screenshot](https://github.com/dsan-io/personalWeb/blob/main/assets/images/webPageMobile.webp)

> ⚠️ **Proyecto en construcción.** Este sitio está en desarrollo activo y recibe mejoras continuas. Este README es provisional y se irá actualizando conforme el proyecto avance.

## 📋 Descripción

Mi portafolio personal. Soy estudiante de Ingeniería en Sistemas Computacionales que orienta su formación hacia el desarrollo web.

Desarrollo proyectos con HTML, CSS y JavaScript para fortalecer mis habilidades, aplicar mis conocimientos y documentar lo que aprendo. Me interesa crear sitios claros, funcionales y fáciles de usar, cuidando tanto su estructura como su presentación.

Este sitio reúne mi perfil, las tecnologías con las que trabajo, mis proyectos y mi currículum. Busco una estadía profesional donde pueda contribuir, recibir orientación y seguir creciendo como desarrollador.

El objetivo del sitio es presentar:

- Información sobre mi formación y perfil profesional.
- Proyectos desarrollados como práctica y aprendizaje.
- Formas de contacto (GitHub, LinkedIn, correo).

## 🚧 Estado actual y mejoras continuas

El proyecto está desarrollo activo. Las mejoras incorporadas incluyen:

- Rediseño de la sección Hero: actualización de la fotografía, la presentación personal, los botones y la distribución del contenido.
- Menú de navegación responsive: apertura y cierre en pantallas pequeñas, alternancia de iconos y cierre al seleccionar un enlace.
- Mejoras de accesibilidad en la navegación: actualización de aria-expanded, cierre con la tecla Escape y devolución del foco al botón del menú.
- Currículum integrado: vista previa del PDF y opciones para abrirlo o descargarlo.
- Copia del correo al portapapeles: botón con confirmación visual y control del tiempo de respuesta tras pulsaciones repetidas.
- Actualización visual: incorporación de un logotipo y ajustes en botones, tarjetas, etiquetas y superficies.
- Organización modular de CSS: separación de estilos base, distribución, componentes y utilidades, con capas de cascada y variables de diseño.
- Ajustes responsive: mejoras en la distribución y los espacios para diferentes tamaños de pantalla.

El portafolio seguirá ampliándose con nuevos proyectos y ajustes de diseño, contenido y accesibilidad.

## 🛠️ Tecnologías utilizadas

- **HTML5**: estructura semántica y organización del contenido.
- **CSS3**: Grid, Flexbox, media queries, variables personalizadas, anidamiento nativo y capas de cascada con @layer.
- **JavaScript**: interacción del menú y confirmación al copiar el correo.
- **Clipboard API**: copia del correo al portapapeles.
- **Lucide**: iconos de navegación, acciones y contacto.
- **Google Fonts** — Plus Jakarta Sans: tipografía del sitio.
- **pnpm**: gestión de dependencias.
- **Git y GitHub**: control de versiones y alojamiento del código.

## 📁 Estructura del proyecto

```
personalWeb/
├── assets/
│   ├── images/                  # Fotografías, logotipo y capturas
│   └── cv_sandoval_leonardo.pdf
├── js/
│   └── app.js                   # Menú y copia del correo
├── styles/
│   ├── base/
│   │   ├── _global.css
│   │   ├── _reset.css
│   │   ├── _tokens.css
│   │   └── _typography.css
│   ├── components/
│   │   ├── _button.css
│   │   ├── _card.css
│   │   ├── _skill-tag.css
│   │   └── _surface.css
│   ├── layout/
│   │   ├── _header.css
│   │   └── _layout.css
│   ├── utilities/
│   │   └── _utilities.css
│   └── styles.css               # Importaciones y orden de capas
├── .gitignore
├── index.html
├── package.json
├── pnpm-lock.yaml
└── README.md
```

## 🚀 Cómo verlo localmente

1. Clona el repositorio:
   ```bash
   git clone https://github.com/dsan-io/personalWeb.git
   ```
2. Abre el archivo `index.html` en tu navegador, o usa una extensión como **Live Server** en VS Code para recarga automática.

## 📬 Contacto

- **GitHub:** [dsan-io](https://github.com/dsan-io)
- **LinkedIn:** [in/leonardosandoval](https://linkedin.com/in/leonardosandoval)
- **Email:** l.sandoval.dev@gmail.com

---

_Este README se actualizará con capturas de pantalla, demo en vivo y documentación más detallada conforme el proyecto se estabilice._
