import os
import json
import logging
from pydantic import BaseModel, ValidationError
import paho.mqtt.client as mqtt
from utils.database import guardar_datos_calidad_aire

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('procesador')

# Configuración MQTT y PostgreSQL
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "calidad_aire/ciudades"

# Modelo Pydantic
class AirQualityData(BaseModel):
    pais: str
    ciudad: str
    valor_calidad_aire: int
    categoria_calidad_aire: str
    categoria_monoxido_carbono: str
    valor_ozono: int
    categoria_ozono: str
    valor_dioxido_nitrogeno: int
    categoria_dioxido_nitrogeno: str
    valor_particulas_finas: int
    categoria_particulas_finas: str

def on_connect(client, userdata, flags, rc):
    logger.info(f"Conectado al broker MQTT con código: {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        validated = AirQualityData(**data)
        logger.info(f"Mensaje validado: {validated}")
        
        # Guardar en la base de datos usando la función de utils/database.py
        resultado = guardar_datos_calidad_aire(validated)
        if resultado:
            logger.info("Datos almacenados correctamente en la base de datos.")
        else:
            logger.error("Error al almacenar datos en la base de datos.")
    except (ValidationError, Exception) as e:
        logger.error(f"Error procesando mensaje: {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    logger.info(f"Conectando a MQTT broker en {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
