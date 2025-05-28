# Proyecto_final

 Miembros del equipo:
 
  - Manel Diaz

  - Rubén Alsasua

  - Eneko Saez

 Enlace GitHub: https://github.com/enekodeusto/proyecto_final
 
 Enlace Word: https://deusto-my.sharepoint.com/:w:/g/personal/r_alsasua_opendeusto_es/EUof5mQc8_NChA_X5iEPl_IBgpLPnO8sqaDGMKqqYBoNWw?e=ZqyaWk
 
 Enlace Power Point: https://deusto-my.sharepoint.com/:p:/g/personal/r_alsasua_opendeusto_es/EUb_1NRfxEpLkN_ovGSpEyAB-BcMIGV93RMSzGHEcbNBYg?e=x7UCVd

## Instrucciones de uso
1. **Clonar el Repositorio**: Mediante el siguiente comando es posible clonar el proyecto: “git clone https://github.com/EnekoDeusto/Proyecto_final.git”
2. **Abrir la carpeta en la que se encuentra el archivo docker-compose.yml**
3. **Levantar contenedores**: Mediante el siguiente comando es posible levantar todos los contenedores para el correcto funcionamiento del proyecto: “docker-compose up –build-d"

    Esto iniciará:
    - Broker MQTT
    - Capturador de datos
    - Procesador/ validador/ almacenamiento
    - Base de datos PostgreSQL
    - Panel Grafana

    Verificar el funcionamiento
    - Para comprobar que los contenedores están corriendo es posible utilizar el siguiente comando: “docker ps”
    - Para comprobar el correcto funcionamiento de los contenedores de Capturador y precesador, es posible visualizar los logs de validación y el almacenamiento en las tablas mediante los siguientes comandos: “docker exec -it Postgres psql -U postgres -d calidad_aire” y “SELECT * FROM calidad_aire LIMIT 5;”
    - Para comprobar de forma precisa la visualizacion se puede acceder a la siguiente URL mediante el navegador: http://localhost:3000. Iniciando sesión con usuario “admin” y contraseña “admin”, es posible ver todos los gráficos. 

