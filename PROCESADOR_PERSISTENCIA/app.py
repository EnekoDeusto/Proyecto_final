import os
import json
import paho.mqtt.client as mqtt

# Parámetros de conexión MQTT
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "calidad_aire/ciudades"

# Función que se ejecuta al conectarse al broker
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código de resultado: " + str(rc))
    client.subscribe(MQTT_TOPIC)

# Función que se ejecuta al recibir un mensaje
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        print(f"[Mensaje recibido] Tópico: {msg.topic} | Datos: {payload}")
        # Aquí podrías validar con Pydantic o guardar en base de datos
    except json.JSONDecodeError:
        print("Error: no se pudo decodificar el mensaje JSON")

# Inicializar cliente
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar y escuchar
print(f"Conectando al broker {MQTT_BROKER}:{MQTT_PORT}...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print(f"Escuchando en el tópico '{MQTT_TOPIC}'...")
client.loop_forever()
