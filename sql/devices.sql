CREATE DATABASE irules;
use irules;
CREATE TABLE devices (
id MEDIUMINT NOT NULL AUTO_INCREMENT,
MAC varchar(5000),
State varchar(5000),
Lastmodified datetime,
Created datetime,
 PRIMARY KEY (id)
)