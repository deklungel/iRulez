CREATE DATABASE irules;
use irules;
CREATE TABLE devices (
id MEDIUMINT NOT NULL AUTO_INCREMENT,
MAC varchar(5000),
State varchar(5000),
Lastmodified datetime,
Naam varchar(1000),
Created datetime,
 PRIMARY KEY (id)
)