import os
import time
import json
import logging
import pandas as pd
import paho.mqtt.client as mqtt

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "calidad_aire/ciudades"

CSV_PATH = "./data/global_air_pollution_data.csv"
df = pd.read_csv(CSV_PATH)

client = mqtt.Client()

def main():
    start_time = time.time()
    total_rows = len(df)
    
    logger.info(f"Conectando al broker MQTT en {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    logger.info("Publicando datos...")
    for idx, row in enumerate(df.iterrows(), 1):
        _, row_data = row
        payload = {
            "pais": row_data["country_name"],
            "ciudad": row_data["city_name"],
            "valor_calidad_aire": row_data["aqi_value"],
            "categoria_calidad_aire": row_data["aqi_category"],
            "categoria_monoxido_carbono": row_data["co_aqi_category"],
            "valor_ozono": row_data["ozone_aqi_value"],
            "categoria_ozono": row_data["ozone_aqi_category"],
            "valor_dioxido_nitrogeno": row_data["no2_aqi_value"],
            "categoria_dioxido_nitrogeno": row_data["no2_aqi_category"],
            "valor_particulas_finas": row_data["pm2.5_aqi_value"],
            "categoria_particulas_finas": row_data["pm2.5_aqi_category"]
        }

        client.publish(MQTT_TOPIC, json.dumps(payload))
        elapsed_time = time.time() - start_time
        
        if idx % 10 == 0 or idx == total_rows:  # Show progress every 10 rows or at the end
            logger.info(f"Progreso: {idx}/{total_rows} filas procesadas ({idx/total_rows*100:.1f}%) - Tiempo transcurrido: {elapsed_time:.2f} segundos")
        
        time.sleep(0.2)

    client.disconnect()
    total_elapsed_time = time.time() - start_time
    logger.info(f"Publicación finalizada. Total: {total_rows} filas en {total_elapsed_time:.2f} segundos")

if __name__ == "__main__":
    main()
