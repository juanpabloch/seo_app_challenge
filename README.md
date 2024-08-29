# Seo app challenge

## Aplicación Web con Docker
## Requisitos Previos
 * Docker: Asegúrate de tener instalado y en funcionamiento Docker en tu sistema. Descarga e instala la versión más reciente desde \[enlace de descarga de Docker\](https://www.docker.com/products/docker-desktop/).
 * Git: Necesitarás Git para clonar el repositorio. Puedes descargarlo desde \[enlace de descarga de Git\](https://git-scm.com/downloads).

## Pasos a Seguir
 * Clona el Repositorio:
   * Abre tu terminal o línea de comandos.
   * Crea una nueva carpeta para tu proyecto:
        mkdir mi-proyecto
     
        cd mi-proyecto

   * Clona el repositorio:
     git clone https://github.com/juanpabloch/seo_app_challenge

 * Configura el Entorno:
    * Copia el archivo .env.example y renómbralo a .env:
        cp .env.example .env
    * API_KEY = 'api key para Pagespeedapi'

    * Edita el archivo .env y completa las variables de entorno necesarias para tu proyecto.
    
* Levanta la Aplicación:
    * Navega hasta el directorio raíz de tu proyecto:
        cd seo_app_challenge

   * Ejecuta el siguiente comando para construir y levantar los contenedores:
     docker-compose -f docker-compose.yaml up --build -d

     * -f docker-compose.yml: Especifica el archivo de configuración de Docker Compose.
     * --build: Reconstruye las imágenes si hay cambios.
     * -d: Ejecuta los contenedores en segundo plano (detached mode).

 * Verifica los Contenedores:
   * Para listar los contenedores en ejecución:
     docker ps

   * Asegúrate de que todos los contenedores estén en estado "Up".
    
    * Accede a la Aplicación:
    * Abre tu navegador web y ve a la siguiente dirección:
     http://127.0.0.1:8000

     Si todo está configurado correctamente, deberías ver la aplicación en funcionamiento.


