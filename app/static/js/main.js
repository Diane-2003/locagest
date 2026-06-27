document.addEventListener("DOMContentLoaded", () => {
    // Confirmation avant suppression / résiliation
    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (e) => {
            const message = form.getAttribute("data-confirm");
            if (!window.confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Fermeture automatique des alertes flash après 5 secondes
    document.querySelectorAll(".alerte").forEach((alerte) => {
        setTimeout(() => {
            alerte.style.transition = "opacity 0.4s";
            alerte.style.opacity = "0";
            setTimeout(() => alerte.remove(), 400);
        }, 5000);
    });

    // Hamburger menu
    const hamburger = document.getElementById("hamburger");
    const navbarMenu = document.getElementById("navbar-menu");
    if (hamburger && navbarMenu) {
        hamburger.addEventListener("click", () => {
            const isOpen = navbarMenu.classList.toggle("open");
            hamburger.classList.toggle("open", isOpen);
            hamburger.setAttribute("aria-expanded", isOpen);
        });
        // Fermer le menu si on clique sur un lien
        navbarMenu.querySelectorAll(".nav-link").forEach(link => {
            link.addEventListener("click", () => {
                navbarMenu.classList.remove("open");
                hamburger.classList.remove("open");
                hamburger.setAttribute("aria-expanded", "false");
            });
        });
    }
});