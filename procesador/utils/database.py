import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurar logger
logger = logging.getLogger('database')

# Configuración de la base de datos
PG_HOST = os.environ.get("POSTGRES_HOST", "db")
PG_PORT = os.environ.get("POSTGRES_PORT", "5432")
PG_USER = os.environ.get("POSTGRES_USER", "postgres")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
PG_DB = os.environ.get("POSTGRES_DB", "postgres")

DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Definir la tabla que corresponde a la estructura en init.sql
calidad_aire_table = Table(
    "calidad_aire",
    metadata,
    Column("id", Integer, primary_key=True),
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

Session = sessionmaker(bind=engine)

def guardar_datos_calidad_aire(datos):
    """
    Guarda los datos de calidad del aire en la base de datos.
    
    Args:
        datos: Instancia de AirQualityData validada por Pydantic
    
    Returns:
        bool: True si la operación fue exitosa, False en caso contrario
    """
    try:
        with Session() as session:
            # Convertir el modelo Pydantic a un diccionario
            datos_dict = datos.dict() if hasattr(datos, 'dict') else datos
            
            # Insertar los datos en la tabla
            ins = calidad_aire_table.insert().values(**datos_dict)
            session.execute(ins)
            session.commit()
            
            logger.info(f"Datos guardados correctamente: {datos_dict['ciudad']}, {datos_dict['pais']}")
            return True
    except Exception as e:
        logger.error(f"Error al guardar datos en la base de datos: {e}")
        return False