CREATE DATABASE IF NOT EXISTS imobiliaria;

USE imobiliaria;

CREATE TABLE IF NOT EXISTS property_type (
	id INT(11) AUTO_INCREMENT,
	name VARCHAR(255),
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS real_estate (
  id INT(11) AUTO_INCREMENT,
  price NUMERIC(10, 2) NOT NULL,
  address VARCHAR(300) NOT NULL,
  neighborhood_city VARCHAR(255) NOT NULL,
  rooms INT(11) NOT NULL,
  garage INT(11) NOT NULL,
  bathroom INT(11) NOT NULL,
  square_meter NUMERIC(10, 2) NOT NULL,
  type_id INT(11) NOT NULL,
  suite BOOLEAN NOT NULL,
  gym BOOLEAN NOT NULL,
  balcony BOOLEAN NOT NULL,
  hall BOOLEAN NOT NULL,
  transaction_type VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (type_id) REFERENCES property_type(id)
);
