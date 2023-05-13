CREATE SCHEMA IF NOT EXISTS imobiliaria;

CREATE table property_type (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

create table if not exists real_estate (
  id SERIAL PRIMARY KEY,
  price NUMERIC(10, 2),
  address TEXT,
  neighborhood_city TEXT,
  rooms INTEGER,
  garage INTEGER,
  bathroom INTEGER,
  square_meter NUMERIC(10, 2),
  type_id INTEGER REFERENCES property_type(id),
  suite BOOLEAN,
  gym BOOLEAN,
  balcony BOOLEAN,
  hall BOOLEAN,
  transaction_type TEXT,
  lat NUMERIC(10, 6),
  long NUMERIC(10, 6)
);