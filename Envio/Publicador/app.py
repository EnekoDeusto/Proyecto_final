import os
import time
import json
import pandas as pd
import paho.mqtt.client as mqtt

# Parámetros de conexión
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "calidad_aire/ciudades"

# Leer el CSV
CSV_PATH = "Datos_calidad_aire/updated_pollution_dataset.csv"  # Asegúrate de que este archivo esté en Publicador/
df = pd.read_csv(CSV_PATH)

# Configurar cliente MQTT
client = mqtt.Client()

def main():
    print(f"Conectando al broker MQTT en {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    print("Publicando datos...")
    for _, row in df.iterrows():
        payload = {
            "Temperatura": row["Temperature"],
            "Humedad": row["Humidity"],
            "Pm2_5": row["PM2.5"],
            "Pm10": row["PM10"],
            "No2": row["NO2"],
            "So2": row["SO2"],
            "Co": row["CO"],
            "Cercania_areas_industriales": row["Proximity_to_Industrial_Areas"],
            "Populacion": row["Population_Density"],
            "Calidad_Aire": row["Air Quality"]
        }

        client.publish(MQTT_TOPIC, json.dumps(payload))
        print(f"Publicado: {payload}")
        time.sleep(1)  # Esperar 1 segundo entre publicaciones

    client.disconnect()
    print("Publicación finalizada.")

if __name__ == "__main__":
    main()
