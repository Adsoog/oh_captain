// Scripts de CSRF, tema oscuro/claro, barra lateral, etc.
document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value
        || document.querySelector('meta[name="csrf-token"]')?.content;
    if (csrfToken) {
        document.body.addEventListener("htmx:configRequest", function (event) {
            event.detail.headers['X-CSRFToken'] = csrfToken;
        });
    }
});

// Alternar el modo oscuro/claro
function toggleTheme() {
    const themeIcon = document.getElementById("theme-icon");
    const currentTheme = document.documentElement.getAttribute("data-theme");

    if (currentTheme === "dark") {
        document.documentElement.setAttribute("data-theme", "light");
        localStorage.setItem("theme", "light");
        themeIcon.classList.replace("bx-sun", "bx-moon");
    } else {
        document.documentElement.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
        themeIcon.classList.replace("bx-moon", "bx-sun");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);

    const themeIcon = document.getElementById("theme-icon");
    if (savedTheme === "dark") {
        themeIcon.classList.replace("bx-moon", "bx-sun");
    } else {
        themeIcon.classList.replace("bx-sun", "bx-moon");
    }
});

document.getElementById("theme-toggle").addEventListener("click", toggleTheme);

// Funcionalidad de la barra lateral
function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");

    if (sidebar.classList.contains("sidebar-expanded")) {
        sidebar.classList.replace("sidebar-expanded", "sidebar-collapsed");
        mainContent.classList.replace("ml-48", "ml-20");
    } else {
        sidebar.classList.replace("sidebar-collapsed", "sidebar-expanded");
        mainContent.classList.replace("ml-20", "ml-48");
    }
}

function toggleSubmenu(id) {
    const submenu = document.getElementById(id);

    if (submenu.classList.contains("open")) {
        submenu.classList.remove("open");
        submenu.style.maxHeight = "0";
    } else {
        document.querySelectorAll(".submenu").forEach(s => {
            s.classList.remove("open");
            s.style.maxHeight = "0";
        });

        submenu.classList.add("open");
        submenu.style.maxHeight = submenu.scrollHeight + "px";
    }
}
