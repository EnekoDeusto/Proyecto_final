DROP TABLE IF EXISTS calidad_aire;

CREATE TABLE IF NOT EXISTS calidad_aire (
    id SERIAL PRIMARY KEY,
    pais VARCHAR,
    ciudad VARCHAR,
    valor_calidad_aire INTEGER,
    categoria_calidad_aire VARCHAR,
    categoria_monoxido_carbono VARCHAR,
    valor_ozono INTEGER,
    categoria_ozono VARCHAR,
    valor_dioxido_nitrogeno INTEGER,
    categoria_dioxido_nitrogeno VARCHAR,
    valor_particulas_finas INTEGER,
    categoria_particulas_finas VARCHAR
);


