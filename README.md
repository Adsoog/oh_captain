```sh
# 🔍 Verificar versiones de npm y Node.js
npm --version  # Verifica la versión de npm
# Salida esperada: 10.9.2

# 📦 Instalación de Tailwind CSS en Django
python manage.py tailwind install

# 🎨 Iniciar el watcher de Tailwind CSS
python manage.py tailwind start

node --version  # Verifica la versión de Node.js
# Salida esperada: v23.6.1

# 🚀 Ejecutar Django con Tailwind en paralelo

# 📌 1️⃣ Terminal 1: Ejecutar Tailwind CSS
python manage.py tailwind start

# 📌 2️⃣ Terminal 2: Ejecutar el servidor de Django
python manage.py runserver 0.0.0.0:8000
python




TURBO JS USAR DESPUES:

    <!-- Turbo.js para navegación sin recarga
    <script type="module" src="https://cdn.jsdelivr.net/npm/@hotwired/turbo@latest/dist/turbo.es2017-esm.min.js"></script>
     Script para manejar la navegación de Turbo.js -->
    <script>
      document.addEventListener("turbo:before-fetch-request", function (event) {
        let turboFrame = event.target;
        if (turboFrame.id === "main-content") {
          history.pushState({}, "", event.detail.fetchOptions.url);
        }
      });

      window.addEventListener("popstate", function (event) {
        Turbo.visit(location.href);
      });
    </script>
    -->


COLOR DE LETRA PARA TODOS

 text-gray-700



commit chiquitillo >.<