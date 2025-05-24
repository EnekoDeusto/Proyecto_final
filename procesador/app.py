import os
import json
from pydantic import BaseModel, ValidationError
import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Configuración MQTT y PostgreSQL
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "calidad_aire/ciudades"

PG_HOST = os.environ.get("POSTGRES_HOST", "db")
PG_PORT = os.environ.get("POSTGRES_PORT", "5432")
PG_USER = os.environ.get("POSTGRES_USER", "postgres")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
PG_DB = os.environ.get("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

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

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
metadata = MetaData()

air_quality_table = Table(
    "air_quality",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("pais", String),
    Column("ciudad", String),
    Column("valor_calidad_aire", Integer),
    Column("categoria_calidad_aire", String),
    Column("categoria_monoxido_carbono", String),
    Column("valor_ozono", Integer),
    Column("categoria_ozono", String),
    Column("valor_dioxido_nitrogeno", Integer),
    Column("categoria_dioxido_nitrogeno", String),
    Column("valor_particulas_finas", Integer),
    Column("categoria_particulas_finas", String),
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con código:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        validated = AirQualityData(**data)
        print("Mensaje validado:", validated)
        # Guardar en la base de datos
        with Session() as session:
            ins = air_quality_table.insert().values(**validated.dict())
            session.execute(ins)
            session.commit()
        print("Datos almacenados en la base de datos.")
    except (ValidationError, Exception) as e:
        print("Error procesando mensaje:", e)

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Conectando a MQTT broker en {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
