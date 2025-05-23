import os
import time
import json
import pandas as pd
import paho.mqtt.client as mqtt

MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "calidad_aire/ciudades"

CSV_PATH = "./data/global_air_pollution_data.csv"
df = pd.read_csv(CSV_PATH)

client = mqtt.Client()

def main():
    print(f"Conectando al broker MQTT en {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    print("Publicando datos...")
    for _, row in df.iterrows():
        payload = {
            "pais": row["country_name"],
            "ciudad": row["city_name"],
            "valor_calidad_aire": row["aqi_value"],
            "categoria_calidad_aire": row["aqi_category"],
            "valor_monoxido_carbono": row["co_aqi_value"],
            "categoria_monoxido_carbono": row["co_aqi_category"],
            "valor_ozono": row["ozone_aqi_value"],
            "categoria_ozono": row["ozone_aqi_category"],
            "valor_dioxido_nitrogeno": row["no2_aqi_value"],
            "categoria_dioxido_nitrogeno": row["no2_aqi_category"],
            "valor_particulas_finas": row["pm2.5_aqi_value"],
            "categoria_particulas_finas": row["pm2.5_aqi_category"]
        }

        client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Publicado: {payload}")
        time.sleep(0.2)

    client.disconnect()
    print("Publicación finalizada.")

if __name__ == "__main__":
    main()
