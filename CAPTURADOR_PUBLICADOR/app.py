import os
import time
import json
import pandas as pd
import paho.mqtt.client as mqtt

MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "calidad_aire/ciudades"

CSV_PATH = "./DATOS/global_air_pollution_data.csv"
df = pd.read_csv(CSV_PATH)

client = mqtt.Client()

def main():
    print(f"Conectando al broker MQTT en {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    print("Publicando datos...")
    for _, row in df.iterrows():
        payload = {
            "country_name": row["country_name"],
            "city_name": row["city_name"],
            "aqi_value": row["aqi_value.5"],
            "aqi_category": row["aqi_category"],
            "co_aqi_value": row["co_aqi_value"],
        }

        client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Publicado: {payload}")
        time.sleep(0.2)

    client.disconnect()
    print("Publicación finalizada.")

if __name__ == "__main__":
    main()
