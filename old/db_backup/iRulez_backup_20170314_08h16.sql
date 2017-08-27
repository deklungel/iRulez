-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: localhost    Database: iRulez
-- ------------------------------------------------------
-- Server version	5.7.17-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Core_Arduino_Outputs`
--

DROP TABLE IF EXISTS `Core_Arduino_Outputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_Arduino_Outputs` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `naam` varchar(32) NOT NULL,
  `omschrijving` text,
  `circuit` varchar(5) DEFAULT NULL,
  `differential` varchar(5) DEFAULT NULL,
  `arduino` int(5) NOT NULL,
  `pin` int(5) NOT NULL,
  `monitor` int(1) NOT NULL DEFAULT '0',
  `telegram` int(1) NOT NULL DEFAULT '0',
  `notification` int(10) DEFAULT NULL,
  `Core_Devices_id` int(10) NOT NULL,
  `hidden` int(1) NOT NULL DEFAULT '0',
  `status` varchar(10) DEFAULT 'OFF',
  `status_time` datetime DEFAULT NULL,
  `notification_snooze` datetime DEFAULT NULL,
  `notification_dismiss` int(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `Arduino` (`arduino`,`pin`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_Arduino_Outputs`
--

LOCK TABLES `Core_Arduino_Outputs` WRITE;
/*!40000 ALTER TABLE `Core_Arduino_Outputs` DISABLE KEYS */;
INSERT INTO `Core_Arduino_Outputs` VALUES (57,'Badkamer','R6/X badkamer ','BB1','30',0,0,0,1,NULL,0,0,'OFF',NULL,NULL,0),(58,'Badkamer - Lavabo','R6/X badkamer lavabo','BB2','30',0,1,0,1,NULL,0,0,'OFF',NULL,NULL,0),(59,'Arduino0/2','R6/4 - Not Connected','NC','NC',0,2,0,0,NULL,0,0,'OFF',NULL,NULL,0),(60,'Zithoek','Dimmer beneden','K1','300',0,3,0,0,NULL,0,0,'OFF',NULL,NULL,0),(61,'Kelder 3','R4/X Kerder achter','AA1','30',0,4,0,1,3600,0,0,'OFF',NULL,NULL,0),(62,'Kamer 2','R3/4 Kamer 2','L3','300',0,5,0,0,NULL,0,0,'OFF',NULL,NULL,0),(63,'Dressing','R3/3 Dressing','L6','300',0,6,0,0,NULL,0,0,'OFF',NULL,NULL,0),(64,'Slaapkamer 1','Dimmer Slaapkamer 1','L5','300',0,7,0,0,NULL,0,0,'OFF',NULL,NULL,0),(65,'Arduino0/8','',NULL,'300',0,8,0,0,NULL,0,0,'OFF',NULL,NULL,0),(66,'Arduino0/9','',NULL,'300',0,9,0,0,NULL,0,0,'OFF',NULL,NULL,0),(67,'Arduino0/10','',NULL,'300',0,10,0,0,NULL,0,0,'OFF',NULL,NULL,0),(68,'Arduino0/11','',NULL,'300',0,11,0,0,NULL,0,0,'OFF',NULL,NULL,0),(69,'Arduino0/12','NIET GEBRUIKEN - Dummy Rolluik2',NULL,'300',0,12,0,0,NULL,0,0,'OFF',NULL,NULL,0),(70,'Arduino0/13','NIET GEBRUIKEN - Dummy Rolluik2',NULL,'300',0,13,0,0,NULL,0,0,'ON','2017-03-14 06:57:01',NULL,0),(71,'Arduino0/14','NIET GEBRUIKEN - Dummy Rolluik1',NULL,'300',0,14,0,0,NULL,0,0,'OFF',NULL,NULL,0),(72,'Arduino0/15','NIET GEBRUIKEN - Dummy Rolluik1',NULL,'300',0,15,0,0,NULL,0,0,'ON','2017-03-14 06:57:00',NULL,0),(73,'Arduino1/0','',NULL,'300',1,0,0,0,NULL,1,0,'OFF',NULL,NULL,0),(74,'Arduino1/1','',NULL,'300',1,1,0,0,NULL,1,0,'OFF',NULL,NULL,0),(75,'Arduino1/2','',NULL,'300',1,2,0,0,NULL,1,0,'OFF',NULL,NULL,0),(76,'Arduino1/3','',NULL,'300',1,3,0,0,NULL,1,0,'OFF',NULL,NULL,0),(77,'Arduino1/4','',NULL,'300',1,4,0,0,NULL,1,0,'OFF',NULL,NULL,0),(78,'Arduino1/5','',NULL,'300',1,5,0,0,NULL,1,0,'OFF',NULL,NULL,0),(79,'Arduino1/6','',NULL,'300',1,6,0,0,NULL,1,0,'OFF',NULL,NULL,0),(80,'Arduino1/7','',NULL,'300',1,7,0,0,NULL,1,0,'OFF',NULL,NULL,0),(81,'Kelder Gang','R5/X Kelder GANG','AA2','30',1,8,0,1,3600,1,0,'OFF',NULL,NULL,0),(82,'Kelder 2','R5/X Wijnkelder','AA4','30',1,9,0,1,3600,1,0,'OFF',NULL,NULL,0),(83,'Berging','R5/X Berging','AA5','30',1,10,0,1,NULL,1,0,'OFF',NULL,NULL,0),(84,'Kelder 1','R5/X Kelder Joke','AA3','30',1,11,0,1,3600,1,0,'OFF',NULL,NULL,0),(85,'Arduino1/12','Rolluik 2 - AF','I2','300',1,12,0,0,NULL,1,0,'OFF',NULL,NULL,0),(86,'Arduino1/13','Rolluik 2 - OP','I2','300',1,13,0,0,NULL,1,0,'OFF',NULL,NULL,0),(87,'Arduino1/14','Rolluik 1 - AF','I1','300',1,14,0,0,NULL,1,0,'OFF',NULL,NULL,0),(88,'Arduino1/15','Rolluik 1 - OP','I1','300',1,15,0,0,NULL,1,0,'OFF',NULL,NULL,0),(89,'Voordeur ','R4/X Buitenverlichting voordeur','Z3','30',2,0,0,0,NULL,2,0,'OFF',NULL,NULL,0),(90,'Terras','R4/X Buitenverlichting Terras','Z2','30',2,1,0,0,NULL,2,0,'ON','2017-03-10 19:04:10',NULL,0),(91,'Zijdeur','R4/X Buitenverlichting Zijdeur','Z1','30',2,2,1,1,10,2,0,'OFF',NULL,NULL,0),(92,'Arduino2/3','R4/3','NC','NC',2,3,0,0,NULL,2,0,'OFF',NULL,NULL,0),(93,'Arduino2/4','NOT CONECTED','NC','NC',2,4,0,0,NULL,2,0,'OFF',NULL,NULL,0),(94,'Arduino2/5','NOT CONECTED','NC','NC',2,5,0,0,NULL,2,0,'OFF',NULL,NULL,0),(95,'WV Beneden','R1/1 WC Benden','K4','300',2,6,0,0,NULL,2,0,'OFF',NULL,NULL,0),(96,'Eetplaats','R1/2 Eetplaats','K2','300',2,7,0,0,NULL,2,0,'OFF',NULL,NULL,0),(97,'Eiland','R1/3 Eiland','K5','300',2,8,0,0,NULL,2,0,'OFF',NULL,NULL,0),(98,'Keuken','R1/4 Keuken','K3','300',2,9,0,0,NULL,2,0,'OFF',NULL,NULL,0),(99,'Trap','R2/1 Trap','K6','300',2,10,0,0,NULL,2,0,'OFF',NULL,NULL,0),(100,'Luster','R2/2 Luster eetplaats','K8','300',2,11,0,0,NULL,2,0,'OFF',NULL,NULL,0),(101,'Gang Beneden','R2/3 Gang Beneden','K7','300',2,12,0,0,NULL,2,0,'OFF',NULL,NULL,0),(102,'Gang Boven','R2/4 Gang Boven','L1','300',2,13,0,0,NULL,2,0,'OFF',NULL,NULL,0),(103,'WC boven','R3/1 WC Boven','L4','300',2,14,0,0,NULL,2,0,'OFF',NULL,NULL,0),(104,'Kamer 3','R3/2 Kamer 3 ','L2','300',2,15,0,0,NULL,2,0,'OFF',NULL,NULL,0);
/*!40000 ALTER TABLE `Core_Arduino_Outputs` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete dependend actions Arduino` AFTER DELETE ON `Core_Arduino_Outputs` FOR EACH ROW DELETE FROM Core_vButtonDB_actions_Arduino WHERE Core_vButtonDB_actions_Arduino.Core_Arduino_Outputs_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete dependent Condition` AFTER DELETE ON `Core_Arduino_Outputs` FOR EACH ROW DELETE FROM Core_vButtonDB_actions_Conditions WHERE Core_vButtonDB_actions_Conditions.Core_Arduino_Outputs_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete dependent FBL` AFTER DELETE ON `Core_Arduino_Outputs` FOR EACH ROW DELETE FROM Core_vButtonDB_actions_FBL WHERE Core_vButtonDB_actions_FBL.Core_Arduino_Outputs_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Core_Devices`
--

DROP TABLE IF EXISTS `Core_Devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_Devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `MAC` varchar(12) NOT NULL,
  `Nummer` varchar(10) NOT NULL,
  `Arduino_Type` int(10) NOT NULL,
  `Versie` varchar(25) DEFAULT NULL,
  `Type` varchar(255) DEFAULT NULL,
  `IP` varchar(15) DEFAULT NULL,
  `Ping` tinyint(1) DEFAULT '10',
  `MQTT` int(5) DEFAULT '10',
  `temperature` double DEFAULT NULL,
  `humidity` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `MAC` (`MAC`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_Devices`
--

LOCK TABLES `Core_Devices` WRITE;
/*!40000 ALTER TABLE `Core_Devices` DISABLE KEYS */;
INSERT INTO `Core_Devices` VALUES (0,'DEADBEEFFEE1','Arduino0',1,'13.1','iRulez_16IO_Board','10.0.40.6',0,0,NULL,NULL),(1,'DEADBEEFFEE2','Arduino1',1,'13.1','iRulez_16IO_Board','10.0.40.4',0,0,NULL,NULL),(2,'DEADBEEFFEE3','arduino2',1,'13.1','iRulez_16IO_Board','10.0.40.5',0,0,NULL,NULL),(3,'Virtual','Arduino3',4,'N/A','N/A','N/A',10,10,NULL,NULL),(4,'abcdefg','Kodi0',3,NULL,NULL,NULL,10,10,NULL,NULL);
/*!40000 ALTER TABLE `Core_Devices` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete Core_Device - Core_vButtonDB` AFTER DELETE ON `Core_Devices` FOR EACH ROW DELETE FROM Core_vButtonDB WHERE Core_vButtonDB.Core_Devices = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete Core_Devices - Radio` AFTER DELETE ON `Core_Devices` FOR EACH ROW DELETE FROM html_Radio WHERE html_Radio.Core_Devices_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `delete from Core_Arduino_Outputs` AFTER DELETE ON `Core_Devices` FOR EACH ROW DELETE FROM Core_Arduino_Outputs WHERE Core_Arduino_Outputs.Core_Devices_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Core_Stats`
--

DROP TABLE IF EXISTS `Core_Stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_Stats` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `id_Core_Arduino_Output` int(5) NOT NULL,
  `Time_on` datetime NOT NULL,
  `Time_off` datetime DEFAULT NULL,
  `DatesON` varchar(254) DEFAULT NULL,
  `time_delta` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_Stats`
--

LOCK TABLES `Core_Stats` WRITE;
/*!40000 ALTER TABLE `Core_Stats` DISABLE KEYS */;
/*!40000 ALTER TABLE `Core_Stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Core_vButtonDB`
--

DROP TABLE IF EXISTS `Core_vButtonDB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `naam` varchar(50) NOT NULL,
  `omschrijving` varchar(255) DEFAULT NULL,
  `Mode` varchar(5) NOT NULL DEFAULT '1',
  `secBetweenActions` int(10) NOT NULL DEFAULT '0',
  `MD` tinyint(1) NOT NULL DEFAULT '0',
  `IdleTime` int(10) NOT NULL DEFAULT '1800',
  `FBL` varchar(5) NOT NULL DEFAULT 'NONE',
  `FBL_Status` varchar(5) NOT NULL DEFAULT 'DOWN',
  `Delay` int(11) NOT NULL DEFAULT '0',
  `arduino` int(2) NOT NULL,
  `pin` int(2) NOT NULL,
  `actie` varchar(255) DEFAULT NULL,
  `Core_Devices` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB`
--

LOCK TABLES `Core_vButtonDB` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB` VALUES (0,'Arduino0/0','Kelder Hal links','3',2,0,0,'FBL','DOWN',0,0,0,'3|2|FBL|R|1|8|T|E|BTF|R|1|8|Off|300|E',0),(1,'Arduino0/1','Kelder 1','1',0,0,0,'FBL','DOWN',0,0,1,'1|FBL|R|1|11|T|E',0),(2,'Arduino0/2','Kelder 2','3',2,0,0,'FBL','DOWN',0,0,2,'3|2|FBL|R|1|9|T|E|BTF|R|1|9|Off|300|E',0),(3,'Arduino0/3','Kelder 3','3',2,0,0,'FBL','DOWN',0,0,3,'3|2|FBL|R|0|4|T|E|BTF|R|0|4|Off|300|E',0),(4,'Arduino0/4','','1',0,0,0,'NONE','DOWN',0,0,4,'',0),(5,'Arduino0/5','','1',0,0,0,'NONE','DOWN',0,0,5,'',0),(6,'Arduino0/6',NULL,'1',0,0,0,'NONE','DOWN',0,0,6,'',0),(7,'Arduino0/7',NULL,'1',0,0,0,'NONE','DOWN',0,0,7,'',0),(8,'Arduino0/8',NULL,'1',0,0,0,'NONE','DOWN',0,0,8,'',0),(9,'Arduino0/9',NULL,'1',0,0,0,'NONE','DOWN',0,0,9,'',0),(10,'Arduino0/10',NULL,'1',0,0,0,'NONE','DOWN',0,0,10,'',0),(11,'Arduino0/11',NULL,'1',0,0,0,'NONE','DOWN',0,0,11,'',0),(12,'Rolluik2 - AF','Rolluik 2 AF - Nog niet aangesloten','1',0,0,0,'CFBL','DOWN',0,0,12,'1|CFBL|R|1|12|Off|1|E|R|0|12|On|0|E|R|0|13|Off|0|E',0),(13,'Rolluik2 - OP','Rolluik 2 OP - Nog niet aangesloten','1',0,0,0,'CFBL','UP',0,0,13,'1|CFBL|R|1|13|Off|1|E|R|0|13|On|0|E|R|0|12|Off|0|E',0),(14,'Rolluik1 - AF','Rolluik 1 AF - Nog niet aangesloten','1',0,0,0,'CFBL','DOWN',0,0,14,'1|CFBL|R|1|14|Off|1|E|R|0|14|On|0|E|R|0|15|Off|0|E',0),(15,'Rolluik1 - OP','Rolluik 1 OP - Nog niet aangesloten','1',0,0,0,'CFBL','UP',0,0,15,'1|CFBL|R|1|15|Off|1|E|R|0|15|On|0|E|R|0|14|Off|0|E',0),(16,'Arduino1/0','Gang Beneden 2/2','1',0,0,0,'FBL','DOWN',0,1,0,'1|FBL|R|2;0;2;2;2|12;3;7;8;9|T|E',1),(17,'Arduino1/1','Keuken - Terras - 3/1','1',0,0,0,'FBL','UP',0,1,1,'1|FBL|R|2|1|T|E',1),(18,'Arduino1/2','Berging 1/2 + Keuken - Berging 3/2 + Berging Buiten 1/2','1',0,0,0,'FBL','DOWN',0,1,2,'1|FBL|R|1|10|T|E',1),(19,'Arduino1/3','Berging 1/1','3',2,0,0,'NONE','DOWN',0,1,3,'3|2|R|0;1;1;1|4;8;9;11|Off|0|E|BTF|R|1|8|Off|300|E',1),(20,'Arduino1/4','Keuken - Terras - 1/2','1',0,0,0,'NONE','DOWN',0,1,4,'1|R|2|8|T|E',1),(21,'Arduino1/5','WC','1',0,0,0,'NONE','DOWN',0,1,5,'1|R|2|6|T|E',1),(22,'Arduino1/6',NULL,'1',0,0,0,'NONE','DOWN',0,1,6,'',1),(23,'Arduino1/7','Gang Beneden 1/1','1',0,0,0,'FBL','DOWN',0,1,7,'1|FBL|R|2|13|T|E',1),(24,'Arduino1/8','Keuken - Terras - 1/1 + Keuken - Berging - 1/1 + Zithoek 2/1','1',0,0,0,'FBL','DOWN',0,1,8,'1|FBL|R|2|9|T|E',1),(25,'Arduino1/9','Keuken - Terras - 2/2 + Keuken - Berging 2/1 + Zithoek 2/2','1',0,0,0,'NONE','DOWN',0,1,9,'1|R|2|11|T|E',1),(26,'Arduino1/10','Keuken - Terras - 2/1 + Keuken - Berging 2/2 + Zithoek 1/2','1',0,0,0,'NONE','DOWN',0,1,10,'1|R|2|7|T|E',1),(27,'Arduino1/11','Keuken - Terras - 3/2 + Keuken - Berging 3/1 + Zithoek 1/1','3',2,0,0,'FBL','DOWN',0,1,11,'3|2|FBL|BD|-1|1000|0|3|E|BTF|BD|100|1000|0|3|T|E',1),(28,'Arduino1/12','Berging Buiten 1/1','1',0,0,0,'NONE','DOWN',0,1,12,'1|R|1;0;2;2|10;3;7;9|T|E',1),(29,'Arduino1/13','Gang Beneden 2/1 + Berging Buiten 2/1 + Berging Buiten 2/2: ALLES UIT','1',0,0,0,'FBL','DOWN',0,1,13,'1|FBL|R|1;2;2;2;2;2;2;2;2;2;2;0;1;1;1;0;0;0;0;0;0;0|11;15;14;13;12;11;9;8;7;6;3;0;10;9;8;7;6;5;4;3;2;1|Off|0|E',1),(30,'Arduino1/14','Gang Beneden 1/2','1',0,0,0,'NONE','DOWN',0,1,14,'1|R|2|12|T|E',1),(31,'Arduino1/15',NULL,'1',0,0,0,'NONE','DOWN',0,1,15,'',1),(32,'Arduino2/0','NOT Connected','1',0,0,0,'NONE','DOWN',0,2,0,'',2),(33,'Arduino2/1',NULL,'1',0,0,0,'NONE','DOWN',0,2,1,'',2),(34,'Arduino2/2',NULL,'1',0,0,0,'NONE','DOWN',0,2,2,'',2),(35,'Arduino2/3',NULL,'1',0,0,0,'NONE','DOWN',0,2,3,'',2),(36,'Arduino2/4','Trap boven 2/2','1',0,0,0,'NONE','DOWN',0,2,4,'1|R|0;0;0;0;0;2;2;2|0;1;5;6;7;13;14;15|Off|0|E',2),(37,'Arduino2/5','Trap boven 1/1','1',0,0,0,'NONE','DOWN',0,2,5,'1|R|2|13|T|E',2),(38,'Arduino2/6','Trap boven 1/2 + Gang Boven','1',0,0,0,'NONE','DOWN',0,2,6,'1|R|2|13|T|E',2),(39,'Arduino2/7','Kamer 3','1',0,0,0,'NONE','DOWN',0,2,7,'1|R|2|15|T|E',2),(40,'Arduino2/8','Kamer 2','1',0,0,0,'NONE','DOWN',0,2,8,'1|R|0|5|T|E',2),(41,'Arduino2/9','WC Boven','1',0,0,0,'NONE','DOWN',0,2,9,'1|R|2|14|T|E',2),(42,'Arduino2/10','Kamer 1 1/1 + Bed','3',3,0,0,'NONE','DOWN',0,2,10,'3|3|BD|-1|1000|0|7|E|BTF|R|0|6|Off|0|E|BD|-1|1000|0|7|T|E',2),(43,'Arduino2/11','Dressing','1',0,0,0,'NONE','DOWN',0,2,11,'1|R|0|6|T|E',2),(44,'Arduino2/12','Trap boven 2/1','1',0,0,0,'NONE','DOWN',0,2,12,'1|R|2|12|T|E',2),(45,'Arduino2/13','Kamer 1 1/2 - ALLES AAN','3',1,0,0,'NONE','DOWN',0,2,13,'3|1|R|1;2;2;2;2;2;2;2;2;2;0;1;1;1;0;0;0;0;0;0|11;15;14;13;12;11;9;8;7;6;0;10;9;8;7;6;5;4;3;1|Off|0|E|BTF|R|0;0;0;0|0;3;5;6|On|0|E',2),(46,'Arduino2/14','Badkamer 1/2','1',0,0,0,'FBL','DOWN',0,2,14,'1|FBL|R|0|1|T|E',2),(47,'Arduino2/15','Badkamer 1/1','1',0,0,0,'FBL','DOWN',0,2,15,'1|FBL|R|0|0|T|E',2),(137,'Virt_Voordeur','Buitenverlichting  AAN ','1',0,0,0,'FBL','DOWN',0,3,0,'1|FBL|R|2|0|T|E',3),(138,'Virt_Zijdeur','Toggle buitenverlichting zijdeur','1',0,0,0,'FBL','DOWN',0,3,1,'1|FBL|R|2|2|T|E',3),(139,'Virt_Trap AAN','Trap AAN','1',0,0,0,'NONE','DOWN',0,3,2,'1|R|2|10|On|0|E',3),(140,'Virt_Trap UIT','Trap UIT','1',0,0,0,'NONE','DOWN',0,3,3,'1|R|2|10|Off|0|E',3),(141,'Virt_UIT Kelder','Alles UIT Kelder','1',0,0,0,'FBL','DOWN',0,3,4,'1|FBL|R|0;1;1;1|4;8;9;11|Off|0|E',3),(142,'Virt_UIT Gelijkvloers','Alles UIT Gelijkvloers','1',0,0,0,'FBL','DOWN',0,3,5,'1|FBL|R|0;1;2;2;2;2;2;2|3;10;6;7;8;9;11;12|Off|0|E',3),(143,'Virt_UIT Verdiep','Alles UIT Verdiep','1',0,0,0,'FBL','DOWN',0,3,6,'1|FBL|R|0;0|0;1|Off|10|E',3),(144,'Virt_Voordeur 5min ','Aan voor 5 min buiten','1',0,0,0,'NONE','DOWN',0,3,7,'1|R|2|0|Off|300|CA|R|2|0|SD;0;30|E',3),(145,'Virt_Buiten_AAN','Buitenverlichting AAN','1',0,0,0,'NONE','DOWN',0,3,8,'1|R|2|0|On|0|E',3),(146,'Virt_Buiten_UIT','Buitenverlichting UIT','1',0,0,0,'NONE','DOWN',0,3,9,'1|R|2|0|Off|0|E',3),(147,'VirtualArduino3/10','Trap','1',0,0,0,'FBL','DOWN',0,3,10,'1|FBL|R|2|10|T|E',3),(148,'Berging_zithoek_AAN','TMP - Licht in berging en zithoek aan','1',0,0,0,'NONE','DOWN',0,3,11,'1|R|0;1|3;10|On|0|E',3),(149,'Berging_zithoek_UIT','TMP - Licht in berging en zithoek uit','1',0,0,0,'NONE','DOWN',0,3,12,'1|R|0;1|3;10|Off|0|E',3),(150,'VirtualArduino3/13','TMP wekker kamer','1',0,0,0,'NONE','DOWN',0,3,13,'1|BD|100|5000|0|7|On|0|E',3),(151,'VirtualArduino3/14',NULL,'1',0,0,1800,'NONE','DOWN',0,3,14,'',3),(152,'VirtualArduino3/15',NULL,'1',0,0,1800,'NONE','DOWN',0,3,15,'',3);
/*!40000 ALTER TABLE `Core_vButtonDB` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete Dependen FBL` AFTER DELETE ON `Core_vButtonDB` FOR EACH ROW DELETE FROM Core_vButtonDB_actions_FBL WHERE Core_vButtonDB_actions_FBL.Core_vButtonDB_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete Owntrack Actions` AFTER DELETE ON `Core_vButtonDB` FOR EACH ROW DELETE FROM Owntracks_action WHERE Owntracks_action.Core_vButtonDB = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete Timer_Actions` AFTER DELETE ON `Core_vButtonDB` FOR EACH ROW DELETE FROM Timer_Actions WHERE Timer_Actions.Core_vButton_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete dependent Action` AFTER DELETE ON `Core_vButtonDB` FOR EACH ROW DELETE FROM Core_vButtonDB_actions WHERE Core_vButtonDB_actions.core_vButtonDB_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete html_vButton` AFTER DELETE ON `Core_vButtonDB` FOR EACH ROW DELETE from html_vButton WHERE html_vButton.vButton_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Core_vButtonDB_FBL`
--

DROP TABLE IF EXISTS `Core_vButtonDB_FBL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_FBL` (
  `code` varchar(5) NOT NULL,
  `omschrijving` varchar(32) NOT NULL,
  `volgorde` int(3) NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_FBL`
--

LOCK TABLES `Core_vButtonDB_FBL` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_FBL` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB_FBL` VALUES ('CFBL','Condition Feedback Light',4),('FBL','Feedback Light',2),('NONE','None',1),('RCFBL','Reverse Condition Feedback Light',5),('RFBL','Reverse Feedback Light',3);
/*!40000 ALTER TABLE `Core_vButtonDB_FBL` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete from Core_vButtonDB FBL` AFTER DELETE ON `Core_vButtonDB_FBL` FOR EACH ROW DELETE FROM Core_vButtonDB WHERE Core_vButtonDB.FBL = Old.code */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Core_vButtonDB_Mode`
--

DROP TABLE IF EXISTS `Core_vButtonDB_Mode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_Mode` (
  `code` varchar(5) NOT NULL,
  `omschrijving` varchar(32) NOT NULL,
  `hide` varchar(255) DEFAULT NULL,
  `display` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_Mode`
--

LOCK TABLES `Core_vButtonDB_Mode` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_Mode` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB_Mode` VALUES ('0','After Release','MultipleActions|motion|SecondAction',NULL),('1','Immediately','MultipleActions|SecondAction','motion'),('3','2the Action','motion','MultipleActions|SecondAction');
/*!40000 ALTER TABLE `Core_vButtonDB_Mode` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete from Core_vButtonDB` AFTER DELETE ON `Core_vButtonDB_Mode` FOR EACH ROW DELETE FROM Core_vButtonDB WHERE Core_vButtonDB.Mode = old.code */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Core_vButtonDB_actions`
--

DROP TABLE IF EXISTS `Core_vButtonDB_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_actions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `core_vButtonDB_id` int(11) NOT NULL,
  `type` varchar(5) NOT NULL,
  `action_nummer` int(11) NOT NULL DEFAULT '1',
  `dim_speed` int(5) DEFAULT NULL,
  `light_level` int(5) DEFAULT NULL,
  `condition` varchar(5) DEFAULT 'NONE',
  `SD` tinyint(1) NOT NULL DEFAULT '0',
  `SD_Before` int(5) NOT NULL DEFAULT '0',
  `SD_After` int(5) DEFAULT '0',
  `timer` int(10) DEFAULT NULL,
  `mail` varchar(255) DEFAULT NULL,
  `delay` tinyint(1) DEFAULT '0',
  `kodi_action` varchar(2) DEFAULT NULL,
  `kodi_zender` int(10) DEFAULT NULL,
  `kodi_volume` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_actions`
--

LOCK TABLES `Core_vButtonDB_actions` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_actions` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB_actions` VALUES (2,1,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(19,18,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(21,20,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(22,21,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(27,47,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(28,46,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(30,44,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(31,43,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(33,41,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(34,40,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(35,39,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(36,38,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(37,37,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(47,28,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(48,27,'T',1,1000,100,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(49,26,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(50,25,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(52,138,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(55,141,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(56,142,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(57,15,'OFF',1,NULL,NULL,'NONE',0,0,0,1,'',0,NULL,NULL,NULL),(58,14,'OFF',1,NULL,NULL,'NONE',0,0,0,1,'',0,NULL,NULL,NULL),(59,13,'OFF',1,NULL,NULL,'NONE',0,0,0,1,'',0,NULL,NULL,NULL),(60,12,'OFF',1,NULL,NULL,'NONE',0,0,0,1,'',0,NULL,NULL,NULL),(61,15,'ON',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(62,15,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(63,14,'ON',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(64,14,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(65,12,'ON',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(66,12,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(67,13,'ON',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(68,13,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(69,143,'OFF',1,NULL,NULL,'NONE',0,0,0,10,'',0,NULL,NULL,NULL),(70,144,'OFF',1,NULL,NULL,'CA',1,0,30,300,'',0,NULL,NULL,NULL),(71,27,'BD',2,1000,-1,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(72,17,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(74,45,'ON',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(75,42,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(76,24,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(78,19,'OFF',2,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(79,29,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(81,36,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(82,23,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(83,30,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(84,16,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(85,139,'ON',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(86,140,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(90,137,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(91,145,'ON',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(92,146,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(93,147,'T',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(94,42,'T',1,1000,-1,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(95,42,'BD',2,1000,-1,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(96,45,'OFF',2,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(97,4,'T',1,NULL,NULL,'NONE',0,0,0,NULL,NULL,0,NULL,NULL,NULL),(99,148,'ON',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(100,149,'OFF',1,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(102,150,'ON',1,5000,100,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(105,0,'OFF',1,NULL,NULL,'NONE',0,0,0,300,'',0,NULL,NULL,NULL),(106,19,'OFF',1,NULL,NULL,'NONE',0,0,0,300,'',0,NULL,NULL,NULL),(108,2,'OFF',1,NULL,NULL,'NONE',0,0,0,300,'',0,NULL,NULL,NULL),(109,3,'OFF',1,NULL,NULL,'NONE',0,0,0,300,'',0,NULL,NULL,NULL),(110,2,'T',2,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(111,3,'T',2,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL),(112,0,'T',2,NULL,NULL,'NONE',0,0,0,0,'',0,NULL,NULL,NULL);
/*!40000 ALTER TABLE `Core_vButtonDB_actions` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete From Conditions` AFTER DELETE ON `Core_vButtonDB_actions` FOR EACH ROW DELETE FROM Core_vButtonDB_actions_Conditions WHERE Core_vButtonDB_actions_Conditions.Core_vButtonDB_actions_id = Old.core_vButtonDB_id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete from Core_vButtonDB_actions_Arduino` AFTER DELETE ON `Core_vButtonDB_actions` FOR EACH ROW DELETE FROM Core_vButtonDB_actions_Arduino WHERE Core_vButtonDB_actions_Arduino.Core_vButtonDB_actions_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Core_vButtonDB_actions_Arduino`
--

DROP TABLE IF EXISTS `Core_vButtonDB_actions_Arduino`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_actions_Arduino` (
  `Core_vButtonDB_actions_id` int(5) NOT NULL,
  `Core_Arduino_Outputs_id` int(5) NOT NULL,
  `Master` tinyint(1) DEFAULT NULL,
  `Dimmer` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`Core_vButtonDB_actions_id`,`Core_Arduino_Outputs_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_actions_Arduino`
--

LOCK TABLES `Core_vButtonDB_actions_Arduino` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Arduino` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB_actions_Arduino` VALUES (2,84,0,0),(19,83,0,0),(21,97,0,0),(22,95,0,0),(27,57,0,0),(28,58,0,0),(30,101,0,0),(31,63,0,0),(33,103,0,0),(34,62,0,0),(35,104,0,0),(36,102,0,0),(37,102,0,0),(47,60,0,0),(47,83,1,0),(47,96,0,0),(47,98,0,0),(48,60,0,1),(49,96,0,0),(50,100,0,0),(52,91,0,0),(55,61,0,0),(55,81,0,0),(55,82,0,0),(55,84,0,0),(56,60,0,0),(56,83,0,0),(56,95,0,0),(56,96,0,0),(56,97,0,0),(56,98,0,0),(56,100,0,0),(56,101,0,0),(57,88,0,0),(58,87,0,0),(59,86,0,0),(60,85,0,0),(61,72,0,0),(62,71,0,0),(63,71,0,0),(64,72,0,0),(65,69,0,0),(66,70,0,0),(67,70,0,0),(68,69,0,0),(69,57,0,0),(69,58,0,0),(70,89,0,0),(71,60,0,1),(72,90,0,0),(74,57,0,0),(74,60,0,0),(74,62,0,0),(74,63,0,0),(75,63,0,0),(76,98,0,0),(78,61,0,0),(78,81,0,0),(78,82,0,0),(78,84,0,0),(79,57,0,0),(79,58,0,0),(79,59,0,0),(79,60,0,0),(79,61,0,0),(79,62,0,0),(79,63,0,0),(79,64,0,0),(79,81,0,0),(79,82,0,0),(79,83,0,0),(79,84,0,0),(79,92,0,0),(79,95,0,0),(79,96,0,0),(79,97,0,0),(79,98,0,0),(79,100,0,0),(79,101,0,0),(79,102,0,0),(79,103,0,0),(79,104,0,0),(81,57,0,0),(81,58,0,0),(81,62,0,0),(81,63,0,0),(81,64,0,0),(81,102,0,0),(81,103,0,0),(81,104,0,0),(82,102,0,0),(83,101,0,0),(84,60,0,0),(84,96,0,0),(84,97,0,0),(84,98,0,0),(84,101,1,0),(85,99,0,0),(86,99,0,0),(90,89,0,0),(91,89,0,0),(92,89,0,0),(93,99,0,0),(94,64,0,1),(95,64,0,1),(96,57,0,0),(96,58,0,0),(96,60,0,0),(96,61,0,0),(96,62,0,0),(96,63,0,0),(96,64,0,0),(96,81,0,0),(96,82,0,0),(96,83,0,0),(96,84,0,0),(96,95,0,0),(96,96,0,0),(96,97,0,0),(96,98,0,0),(96,100,0,0),(96,101,0,0),(96,102,0,0),(96,103,0,0),(96,104,0,0),(99,60,0,0),(99,83,0,0),(100,60,0,0),(100,83,0,0),(102,64,0,1),(105,81,0,0),(106,81,0,0),(108,82,0,0),(109,61,0,0),(110,82,0,0),(111,61,0,0),(112,81,0,0);
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Arduino` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Core_vButtonDB_actions_Condition`
--

DROP TABLE IF EXISTS `Core_vButtonDB_actions_Condition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_actions_Condition` (
  `code` varchar(5) NOT NULL,
  `omschrijving` varchar(32) NOT NULL,
  `volgorde` int(1) NOT NULL,
  `enable` varchar(255) DEFAULT NULL,
  `disable` varchar(255) DEFAULT NULL,
  `hide` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_actions_Condition`
--

LOCK TABLES `Core_vButtonDB_actions_Condition` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Condition` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB_actions_Condition` VALUES ('CA','Condition AND',3,'con$[]',NULL,''),('CO','Condition OR',2,'con$[]',NULL,''),('NONE','None',1,NULL,'con$[]|SD_Before*|SD_After*','SD_Before*|SD_After*');
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Condition` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete Core_vButtonDB_actions Condition` AFTER DELETE ON `Core_vButtonDB_actions_Condition` FOR EACH ROW DELETE FROM Core_vButtonDB_actions WHERE Core_vButtonDB_actions.condition = old.code */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Core_vButtonDB_actions_Condition_Waypoint`
--

DROP TABLE IF EXISTS `Core_vButtonDB_actions_Condition_Waypoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_actions_Condition_Waypoint` (
  `Core_vButtonDB_actions` int(10) NOT NULL,
  `OwnTracks_Waypoint` int(10) NOT NULL,
  `Soort` varchar(50) DEFAULT NULL,
  UNIQUE KEY `Core_vButtonDB_actions` (`Core_vButtonDB_actions`,`OwnTracks_Waypoint`,`Soort`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_actions_Condition_Waypoint`
--

LOCK TABLES `Core_vButtonDB_actions_Condition_Waypoint` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Condition_Waypoint` DISABLE KEYS */;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Condition_Waypoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Core_vButtonDB_actions_Conditions`
--

DROP TABLE IF EXISTS `Core_vButtonDB_actions_Conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_actions_Conditions` (
  `Core_vButtonDB_actions_id` int(5) NOT NULL,
  `Core_Arduino_Outputs_id` int(5) NOT NULL,
  `ON_OFF` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_actions_Conditions`
--

LOCK TABLES `Core_vButtonDB_actions_Conditions` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Conditions` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB_actions_Conditions` VALUES (98,90,'ON'),(70,89,'ON');
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Conditions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Core_vButtonDB_actions_FBL`
--

DROP TABLE IF EXISTS `Core_vButtonDB_actions_FBL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_actions_FBL` (
  `Core_vButtonDB_id` int(5) NOT NULL,
  `Core_Arduino_Outputs_id` int(5) NOT NULL,
  PRIMARY KEY (`Core_vButtonDB_id`,`Core_Arduino_Outputs_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_actions_FBL`
--

LOCK TABLES `Core_vButtonDB_actions_FBL` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_FBL` DISABLE KEYS */;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_FBL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Core_vButtonDB_actions_Kodi`
--

DROP TABLE IF EXISTS `Core_vButtonDB_actions_Kodi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_actions_Kodi` (
  `Core_vButtonDB_actions_id` int(10) NOT NULL,
  `html_Radio_id` int(10) NOT NULL,
  PRIMARY KEY (`Core_vButtonDB_actions_id`,`html_Radio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_actions_Kodi`
--

LOCK TABLES `Core_vButtonDB_actions_Kodi` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Kodi` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB_actions_Kodi` VALUES (4,0),(5,0),(6,0);
/*!40000 ALTER TABLE `Core_vButtonDB_actions_Kodi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Core_vButtonDB_actions_type`
--

DROP TABLE IF EXISTS `Core_vButtonDB_actions_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Core_vButtonDB_actions_type` (
  `code` varchar(5) NOT NULL,
  `omschrijving` varchar(32) NOT NULL,
  `action` int(1) NOT NULL,
  `volgorde` int(11) NOT NULL,
  `enable` varchar(255) DEFAULT NULL,
  `disable` varchar(255) DEFAULT NULL,
  `show` varchar(255) DEFAULT NULL,
  `hide` varchar(255) DEFAULT NULL,
  `checkEnableDisable` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Core_vButtonDB_actions_type`
--

LOCK TABLES `Core_vButtonDB_actions_type` WRITE;
/*!40000 ALTER TABLE `Core_vButtonDB_actions_type` DISABLE KEYS */;
INSERT INTO `Core_vButtonDB_actions_type` VALUES ('BD','Dimmer',2,4,'','timer$[*]',NULL,'TypeActionDimmer$[*]','TypeActionDimmer$[*];DimSpeed$[*]|TypeActionDimmer$[*];LightValue$[*]'),('K','Kodi',1,5,NULL,NULL,NULL,NULL,NULL),('OFF','OFF',1,3,'timer$[*]','','TypeActionDimmer$[*]',NULL,NULL),('ON','ON',1,2,'timer$[*]','','TypeActionDimmer$[*]',NULL,NULL),('T','Toggle',1,1,NULL,'timer$[*]','TypeActionDimmer$[*]',NULL,NULL);
/*!40000 ALTER TABLE `Core_vButtonDB_actions_type` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `DELETE Core_vButtonDB_actions Type` AFTER DELETE ON `Core_vButtonDB_actions_type` FOR EACH ROW DELETE FROM Core_vButtonDB_actions WHERE Core_vButtonDB_actions.type = old.code */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `Device_Template`
--

DROP TABLE IF EXISTS `Device_Template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Device_Template` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `Naam` varchar(50) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `DefaultName` varchar(50) NOT NULL,
  `Input` int(5) NOT NULL DEFAULT '16',
  `Output` int(5) NOT NULL DEFAULT '16',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Device_Template`
--

LOCK TABLES `Device_Template` WRITE;
/*!40000 ALTER TABLE `Device_Template` DISABLE KEYS */;
INSERT INTO `Device_Template` VALUES (1,'iRBoard','Arduino','Arduino',16,16),(2,'iRRadio','Arduino','Radio',8,8),(3,'Kodi','Kodi','Kodi',0,0),(4,'Virtual Inputs','Arduino','VirtualArduino',16,0);
/*!40000 ALTER TABLE `Device_Template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Monitor_Devices`
--

DROP TABLE IF EXISTS `Monitor_Devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Monitor_Devices` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `ownTracksID` varchar(50) NOT NULL,
  `IP` varchar(15) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `ping` int(2) DEFAULT '10',
  `last_seen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Monitor_Devices`
--

LOCK TABLES `Monitor_Devices` WRITE;
/*!40000 ALTER TABLE `Monitor_Devices` DISABLE KEYS */;
INSERT INTO `Monitor_Devices` VALUES (1,'oneplusLaurent','','Gsm Laurent',10,NULL);
/*!40000 ALTER TABLE `Monitor_Devices` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete depependant` AFTER DELETE ON `Monitor_Devices` FOR EACH ROW DELETE FROM Owntracks_action WHERE Owntracks_action.Monitor_Devices_id = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `OwnTracks_User_Status`
--

DROP TABLE IF EXISTS `OwnTracks_User_Status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OwnTracks_User_Status` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `waypoint_ID` int(10) NOT NULL,
  `Monitor_Devices_ID` int(10) NOT NULL,
  `Status` varchar(50) NOT NULL DEFAULT 'Unknown',
  PRIMARY KEY (`id`),
  UNIQUE KEY `waypoint_ID` (`waypoint_ID`,`Monitor_Devices_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OwnTracks_User_Status`
--

LOCK TABLES `OwnTracks_User_Status` WRITE;
/*!40000 ALTER TABLE `OwnTracks_User_Status` DISABLE KEYS */;
INSERT INTO `OwnTracks_User_Status` VALUES (2,2,1,'OUT');
/*!40000 ALTER TABLE `OwnTracks_User_Status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OwnTracks_Waypoint`
--

DROP TABLE IF EXISTS `OwnTracks_Waypoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OwnTracks_Waypoint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Naam` varchar(50) NOT NULL,
  `Description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OwnTracks_Waypoint`
--

LOCK TABLES `OwnTracks_Waypoint` WRITE;
/*!40000 ALTER TABLE `OwnTracks_Waypoint` DISABLE KEYS */;
INSERT INTO `OwnTracks_Waypoint` VALUES (2,'Thuis','Thuis');
/*!40000 ALTER TABLE `OwnTracks_Waypoint` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete From Event` AFTER DELETE ON `OwnTracks_Waypoint` FOR EACH ROW DELETE from OwnTracks_User_Status where OwnTracks_User_Status.waypoint_ID = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete from Action` AFTER DELETE ON `OwnTracks_Waypoint` FOR EACH ROW DELETE FROM Owntracks_action WHERE Owntracks_action.OwnTracks_Waypoint = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `OwnTracks_event`
--

DROP TABLE IF EXISTS `OwnTracks_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OwnTracks_event` (
  `Naam` varchar(50) NOT NULL,
  `Omschrijving` varchar(50) NOT NULL,
  PRIMARY KEY (`Naam`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OwnTracks_event`
--

LOCK TABLES `OwnTracks_event` WRITE;
/*!40000 ALTER TABLE `OwnTracks_event` DISABLE KEYS */;
INSERT INTO `OwnTracks_event` VALUES ('enter','Enter'),('leave','Leave');
/*!40000 ALTER TABLE `OwnTracks_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Owntracks_action`
--

DROP TABLE IF EXISTS `Owntracks_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Owntracks_action` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `Monitor_Devices_id` int(10) NOT NULL,
  `OwnTracks_Waypoint` int(10) NOT NULL,
  `Core_vButtonDB` int(10) NOT NULL,
  `OwnTracks_event` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Owntracks_action`
--

LOCK TABLES `Owntracks_action` WRITE;
/*!40000 ALTER TABLE `Owntracks_action` DISABLE KEYS */;
INSERT INTO `Owntracks_action` VALUES (1,1,2,144,'enter');
/*!40000 ALTER TABLE `Owntracks_action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Settings`
--

DROP TABLE IF EXISTS `Settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Setting` varchar(32) NOT NULL,
  `value` varchar(255) NOT NULL,
  `example` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Settings`
--

LOCK TABLES `Settings` WRITE;
/*!40000 ALTER TABLE `Settings` DISABLE KEYS */;
INSERT INTO `Settings` VALUES (1,'supervisor','http://10.0.40.1:9001',NULL),(2,'loglevel','debug','info | debug'),(3,'MQTT_ip_address','10.0.40.1',NULL),(4,'MQTT_port','10001','10001'),(5,'MQTT_port_python','1883','1883'),(6,'Notification Method','notification','notification | alert'),(7,'NotificationSnooze','30','60'),(8,'TimeBetweenNotification','30',NULL),(9,'BotID','211680352',NULL),(10,'TokenBOT','214505294:AAErlxY_vYvThW9lA0wVnEkyWyyTa1ZAZ1U',NULL),(11,'Update_Server','http://laurentm.allowed.org:81/WebServiceSOAP/server.php','http://laurentmichel.duckdns.org:81/WebServiceSOAP/server.php'),(12,'websiteLocation','/var/www/html/','/var/www/html/'),(13,'PlayListURL','http://10.0.40.1/radio/playlist',NULL),(14,'MonitorTimeout','15','15'),(15,'MQTT_GATE_ip_address','10.0.50.4',NULL),(16,'MQTT_GATE_port','1883',NULL),(17,'MQTT_Gate_Username','iRulez','iRulez'),(18,'MQTT_Gate_Password','iRulez4ever',''),(19,'Location','Brussels','Brussels');
/*!40000 ALTER TABLE `Settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Timer_Actions`
--

DROP TABLE IF EXISTS `Timer_Actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Timer_Actions` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `Naam` varchar(32) NOT NULL,
  `Time` varchar(12) NOT NULL,
  `Time2` varchar(12) NOT NULL DEFAULT '00:00',
  `Random` tinyint(1) NOT NULL DEFAULT '0',
  `Timer_Day` varchar(32) DEFAULT NULL,
  `Core_vButton_id` int(5) NOT NULL,
  `enabled` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Timer_Actions`
--

LOCK TABLES `Timer_Actions` WRITE;
/*!40000 ALTER TABLE `Timer_Actions` DISABLE KEYS */;
INSERT INTO `Timer_Actions` VALUES (3,'Rolluik 1 OP','sunrise','00:00',0,'1|2|3|4|5|6|7',15,1),(4,'Rolluik 2 OP','sunrise','00:00',0,'1|2|3|4|5|6|7',13,1),(6,'Rolluik 1 AF','sunset+30','00:00',0,'1|2|3|4|5|6|7',14,1),(7,'Rolluik 2 AF','sunset+30','00:00',0,'1|2|3|4|5|6|7',12,1),(8,'Trap AAN','20:00','00:00',0,'1|2|3|4|5|6|7',139,1),(9,'Trap UIT','00:00','00:00',0,'1|2|3|4|5|6|7',140,1),(10,'Buiten AAN - Avond','sunset+60','00:00',0,'1|2|3|4|5|6|7',145,1),(11,'Buiten UIT - Avond','00:00','00:00',0,'1|2|3|4|5|6|7',146,1),(12,'Buiten AAN - Ochtend','sunrise-120','00:00',0,'1|2|3|4|5|6|7',145,1),(13,'Buiten UIt - Ochtend','sunrise','00:00',0,'1|2|3|4|5|6|7',146,1),(20,'TMP - Disney','sunset+30','00:00',0,'6',148,1),(21,'TMP - Disney','23:00','00:00',0,'6',29,1);
/*!40000 ALTER TABLE `Timer_Actions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Timer_Day`
--

DROP TABLE IF EXISTS `Timer_Day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Timer_Day` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `Name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Timer_Day`
--

LOCK TABLES `Timer_Day` WRITE;
/*!40000 ALTER TABLE `Timer_Day` DISABLE KEYS */;
INSERT INTO `Timer_Day` VALUES (1,'Maandag'),(2,'Dinsdag'),(3,'Woensdag'),(4,'Donderdag'),(5,'Vrijdag'),(6,'Zaterdag'),(7,'Zondag');
/*!40000 ALTER TABLE `Timer_Day` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_Radio`
--

DROP TABLE IF EXISTS `html_Radio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_Radio` (
  `id` int(10) NOT NULL,
  `naam` varchar(32) NOT NULL,
  `omschrijving` text,
  `verdiep_id` int(5) DEFAULT NULL,
  `favoriet` int(1) NOT NULL DEFAULT '0',
  `Core_Devices_id` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_Radio`
--

LOCK TABLES `html_Radio` WRITE;
/*!40000 ALTER TABLE `html_Radio` DISABLE KEYS */;
INSERT INTO `html_Radio` VALUES (0,'Kodi0',NULL,NULL,0,4);
/*!40000 ALTER TABLE `html_Radio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_Radio_playlist_Zender`
--

DROP TABLE IF EXISTS `html_Radio_playlist_Zender`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_Radio_playlist_Zender` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `Naam` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `html_Radio_playlist` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_Radio_playlist_Zender`
--

LOCK TABLES `html_Radio_playlist_Zender` WRITE;
/*!40000 ALTER TABLE `html_Radio_playlist_Zender` DISABLE KEYS */;
INSERT INTO `html_Radio_playlist_Zender` VALUES (44,'Stan Van Samang - goeiemorgend, goeiendag','https://www.youtube.com/watch?v=miu73xAKoIo',11);
/*!40000 ALTER TABLE `html_Radio_playlist_Zender` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_Radio_zender_Soort`
--

DROP TABLE IF EXISTS `html_Radio_zender_Soort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_Radio_zender_Soort` (
  `Glyphicon` varchar(30) NOT NULL,
  `Naam` varchar(25) NOT NULL,
  PRIMARY KEY (`Glyphicon`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_Radio_zender_Soort`
--

LOCK TABLES `html_Radio_zender_Soort` WRITE;
/*!40000 ALTER TABLE `html_Radio_zender_Soort` DISABLE KEYS */;
INSERT INTO `html_Radio_zender_Soort` VALUES ('fa-list-ul','Playlist'),('fa-music ','Radio'),('fa-youtube','Youtube');
/*!40000 ALTER TABLE `html_Radio_zender_Soort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_Radio_zenders`
--

DROP TABLE IF EXISTS `html_Radio_zenders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_Radio_zenders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `naam` varchar(50) NOT NULL,
  `url` varchar(100) NOT NULL,
  `soort` varchar(25) NOT NULL,
  `ShortName` varchar(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_Radio_zenders`
--

LOCK TABLES `html_Radio_zenders` WRITE;
/*!40000 ALTER TABLE `html_Radio_zenders` DISABLE KEYS */;
INSERT INTO `html_Radio_zenders` VALUES (1,'Qmusic','http://icecast-qmusic.cdp.triple-it.nl/Qmusic_be_live_96.mp3','fa-music ','Q'),(2,'MNM','http://mp3.streampower.be/mnm_hits-high.mp3','fa-music ','MNM'),(3,'Radio1','http://mp3.streampower.be/radio1_classics-high.mp3','fa-music ','R1'),(4,'Radio2','http://mp3.streampower.be/ra2vlb-high.mp3','fa-music ','R2'),(5,'Studio Brussel','http://mp3.streampower.be/stubru-high.mp3','fa-music ','STUBR'),(6,'Sporza','http://mp3.streampower.be/sporza-high','fa-music ','SPORZ'),(7,'Stan Van Samang - goeiemorgend, goeiendag','https://www.youtube.com/watch?v=miu73xAKoIo','fa-youtube','YT1'),(11,'Rustige Muziek','http://10.50.250.10/radio/playlist/RustigeMuziek.m3u','fa-list-ul','PL1');
/*!40000 ALTER TABLE `html_Radio_zenders` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `Delete from Playlist` AFTER DELETE ON `html_Radio_zenders` FOR EACH ROW DELETE from html_Radio_playlist_Zender WHERE html_Radio_playlist_Zender.html_Radio_playlist = old.id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `html_glyphicon`
--

DROP TABLE IF EXISTS `html_glyphicon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_glyphicon` (
  `code` varchar(32) NOT NULL,
  `naam` varchar(32) NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_glyphicon`
--

LOCK TABLES `html_glyphicon` WRITE;
/*!40000 ALTER TABLE `html_glyphicon` DISABLE KEYS */;
INSERT INTO `html_glyphicon` VALUES (' fa-clock-o','Klok'),('fa-heart','Hart'),('fa-lightbulb-o','Lamp'),('fa-moon-o','Maan'),('fa-music','Muziek'),('fa-power-off','Stopcontact'),('fa-sun-o','Zon');
/*!40000 ALTER TABLE `html_glyphicon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_space`
--

DROP TABLE IF EXISTS `html_space`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_space` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `html_verdiep` int(5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_space`
--

LOCK TABLES `html_space` WRITE;
/*!40000 ALTER TABLE `html_space` DISABLE KEYS */;
INSERT INTO `html_space` VALUES (1,'Living',2),(2,'Keuken',2);
/*!40000 ALTER TABLE `html_space` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_vButton`
--

DROP TABLE IF EXISTS `html_vButton`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_vButton` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `naam` varchar(32) NOT NULL,
  `omschrijving` text,
  `glyphicon` varchar(32) NOT NULL,
  `favoriet` int(1) NOT NULL DEFAULT '0',
  `verdiep_id` int(5) NOT NULL,
  `button_soort_id` int(5) NOT NULL,
  `vButton_id` int(5) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_vButton`
--

LOCK TABLES `html_vButton` WRITE;
/*!40000 ALTER TABLE `html_vButton` DISABLE KEYS */;
INSERT INTO `html_vButton` VALUES (1,'Straatkant',NULL,'fa-lightbulb-o',0,5,1,137),(2,'Zijdeur',NULL,'fa-lightbulb-o',0,5,1,138),(3,'Terras',NULL,'fa-lightbulb-o',0,5,1,17),(4,'Alles uit',NULL,'fa-lightbulb-o',1,2,1,29),(5,'UIT',NULL,'fa-lightbulb-o',0,1,1,141),(6,'UIT',NULL,'fa-lightbulb-o',0,2,1,142),(7,'Rolluik Schuifraam - OP',NULL,'fa-sun-o',0,2,5,15),(8,'Rolluik Schuifraam - AF',NULL,'fa-moon-o',0,2,5,14),(9,'Rolluik grootvast raam - OP',NULL,'fa-sun-o',0,2,5,13),(10,'Rolluik grootvast raam - AF',NULL,'fa-moon-o',0,2,5,12),(12,'Berging',NULL,'fa-lightbulb-o',0,2,1,18),(13,'Trap',NULL,'fa-lightbulb-o',0,1,1,0),(14,'Jokes Kelder',NULL,'fa-lightbulb-o',0,1,1,1),(15,'Achterkelder',NULL,'fa-lightbulb-o',0,1,1,3),(16,'Badkamer',NULL,'fa-lightbulb-o',0,3,1,31),(17,'Lavabo',NULL,'fa-lightbulb-o',0,3,1,46),(18,'Wijnkelder',NULL,'fa-lightbulb-o',0,1,1,2),(19,'Zithoek',NULL,'fa-lightbulb-o',1,2,1,27),(20,'Gang',NULL,'fa-lightbulb-o',1,2,1,23),(21,'Trap',NULL,'fa-lightbulb-o',0,3,1,147),(22,'Dessing',NULL,'fa-lightbulb-o',0,3,1,43),(23,'Kamer 1',NULL,'fa-heart',0,3,1,42);
/*!40000 ALTER TABLE `html_vButton` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_vButton_soort`
--

DROP TABLE IF EXISTS `html_vButton_soort`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_vButton_soort` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `naam` varchar(35) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_vButton_soort`
--

LOCK TABLES `html_vButton_soort` WRITE;
/*!40000 ALTER TABLE `html_vButton_soort` DISABLE KEYS */;
INSERT INTO `html_vButton_soort` VALUES (1,'Verlichting'),(2,'Stopcontact'),(3,'Sfeer'),(4,'Radio'),(5,'Rolluik');
/*!40000 ALTER TABLE `html_vButton_soort` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_verdiep`
--

DROP TABLE IF EXISTS `html_verdiep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_verdiep` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `naam` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_verdiep`
--

LOCK TABLES `html_verdiep` WRITE;
/*!40000 ALTER TABLE `html_verdiep` DISABLE KEYS */;
INSERT INTO `html_verdiep` VALUES (0,'Favorieten'),(1,'Kelder'),(2,'Gelijkvloers'),(3,'Verdiep'),(4,'Zolder'),(5,'Buiten');
/*!40000 ALTER TABLE `html_verdiep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `html_versions`
--

DROP TABLE IF EXISTS `html_versions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `html_versions` (
  `filename` varchar(254) NOT NULL,
  `version` varchar(10) NOT NULL,
  PRIMARY KEY (`filename`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `html_versions`
--

LOCK TABLES `html_versions` WRITE;
/*!40000 ALTER TABLE `html_versions` DISABLE KEYS */;
INSERT INTO `html_versions` VALUES ('Modules/AutoConfig/AutoConfig.py',' 1.2\n'),('Modules/core/arduino.py',' 5.2\n'),('Modules/core/arduino_DEV.py',' 5.2\n'),('Modules/dummy/dummy.py',' 1.2\n'),('Modules/logger/logger.py',' 1.2\n'),('Modules/monitor/monitor.py',' 1.2\n'),('Modules/monitorDevices/monitorDevices.py',' 1.2\n'),('Modules/statistics/statistics.py',' 1.2\n'),('Modules/telegram/telegram.py',' 1.9\n'),('Modules/timer/timer.py',' 1.1\n'),('Website/html/add_devices.php',' 1.0\n'),('Website/html/add_form/add_form_devices.php',' 1.0 \n'),('Website/html/add_form/add_form_monitor.php',' 1.0 \n'),('Website/html/add_form/add_form_outputs.php',' 1.0 \n'),('Website/html/add_form/add_form_owntrack.php',' 1.0	\n'),('Website/html/add_form/add_form_owntracks_action.php',' 1.0	\n'),('Website/html/add_form/add_form_owntracks_groups.php',' 1.0 \n'),('Website/html/add_form/add_form_owntracks_waypoints.php',' 1.0 \n'),('Website/html/add_form/add_form_PlayList.php',' 1.0 \n'),('Website/html/add_form/add_form_radio.php',' 1.0	\n'),('Website/html/add_form/add_form_radiozender.php',' 1.0	\n'),('Website/html/add_form/add_form_vButton.php',' 1.0	\n'),('Website/html/add_form/add_form_verdiepen.php',' 1.0\n'),('Website/html/add_monitor.php',' 1.0\n'),('Website/html/add_owntracks_action.php',' 1.0\n'),('Website/html/add_owntracks_groups.php',' 1.0\n'),('Website/html/add_owntracks_waypoints.php',' 1.0\n'),('Website/html/add_PlayList.php',' 1.0\n'),('Website/html/add_radiozender.php',' 1.0\n'),('Website/html/add_vbutton.php',' 1.1\n'),('Website/html/add_verdiep.php',' 1.0\n'),('Website/html/add_verdiepen.php',' 1.0\n'),('Website/html/backup.php',' 1.0\n'),('Website/html/createPlayList.php','Unknown'),('Website/html/css/block.css',' 1.4\n'),('Website/html/css/bootstrap.min.css',' 1.0\n'),('Website/html/css/bootstrap_extended.css',' 1.0\n'),('Website/html/css/easy-responsive-tabs.css',' 1.0\n'),('Website/html/css/edit_style.css',' 1.2\n'),('Website/html/css/font-awesome.css',' 1.0\n'),('Website/html/css/font-awesome.min.css',' 1.0\n'),('Website/html/css/jasny-bootstrap-custom.css',' 1.0\n'),('Website/html/css/jasny-bootstrap.css',' 1.0\n'),('Website/html/css/jasny-bootstrap.min.css',' 1.0\n'),('Website/html/css/navmenu.css',' 1.0\n'),('Website/html/css/playlist.css','Unknown'),('Website/html/css/responsive.css',' 1.0\n'),('Website/html/css/roundslider.min.css','Unknown'),('Website/html/delete.php',' 1.0\n'),('Website/html/delete_output.php',' 1.0\n'),('Website/html/delete_playlist.php',' 1.0\n'),('Website/html/delete_radioZender.php',' 1.0\n'),('Website/html/edit.php',' 1.3\n'),('Website/html/editableGrid.php',' 1.0\n'),('Website/html/index.php',' 1.5\n'),('Website/html/js/Chart.js',' 1.0\n'),('Website/html/js/Chart.min.js',' 1.0\n'),('Website/html/js/devices.js',' 1.0\n'),('Website/html/js/easyResponsiveTabs.js',' 1.0\n'),('Website/html/js/editablegrid-2.1.0-b25.js',' 1.0\n'),('Website/html/js/edit_menu.js',' 1.0\n'),('Website/html/js/iRule.js',' 1.8\n'),('Website/html/js/iRule_reload.js',' 1.0\n'),('Website/html/js/iRule_Test.js',' 1.0\n'),('Website/html/js/jasny-bootstrap.js',' 1.0\n'),('Website/html/js/jasny-bootstrap.min.js',' 1.0\n'),('Website/html/js/jquery-2.2.3.min.js',' 1.0\n'),('Website/html/js/jquery-ui.js','Unknown'),('Website/html/js/monitor.js',' 1.0\n'),('Website/html/js/mqttws31.js',' 1.0\n'),('Website/html/js/outputs.js',' 1.0\n'),('Website/html/js/owntracks_action.js',' 1.0\n'),('Website/html/js/owntracks_groups.js',' 1.0\n'),('Website/html/js/owntracks_waypoints.js',' 1.0\n'),('Website/html/js/PlayList.js',' 1.0\n'),('Website/html/js/radio.js',' 1.0\n'),('Website/html/js/radiozender.js',' 1.0\n'),('Website/html/js/roundslider.min.js','Unknown'),('Website/html/js/settings.js',' 1.0\n'),('Website/html/js/table_behaviour.js',' 1.0\n'),('Website/html/js/timer.js',' 1.0\n'),('Website/html/js/vButton.js',' 1.0\n'),('Website/html/js/vButton_actions.js',' 1.0\n'),('Website/html/js/verdiepen.js',' 1.0\n'),('Website/html/js/version.js',' 1.0\n'),('Website/html/js/wizard.js',' 1.1\n'),('Website/html/loaddata_devices.php',' 1.0    \n'),('Website/html/loaddata_monitor.php',' 1.0    \n'),('Website/html/loaddata_outputs.php',' 1.1\n'),('Website/html/loaddata_owntracks_action.php',' 1.0    \n'),('Website/html/loaddata_owntracks_groups.php',' 1.0    \n'),('Website/html/loaddata_owntracks_waypoints.php',' 1.0    \n'),('Website/html/loaddata_PlayList.php',' 1.0    \n'),('Website/html/loaddata_radio.php',' 1.0    \n'),('Website/html/loaddata_radiozender.php',' 1.0    \n'),('Website/html/loaddata_settings.php',' 1.0    \n'),('Website/html/loaddata_vbutton.php',' 1.0    \n'),('Website/html/loaddata_vButton_actions.php',' 1.0     \n'),('Website/html/loaddata_verdiepen.php',' 1.0\n'),('Website/html/logfile.php',' 1.0\n'),('Website/html/monitoring.php','Unknown'),('Website/html/radio/generate.php',' 1.0\n'),('Website/html/radio/playlist.php',' 1.0\n'),('Website/html/radio/station.php',' 1.0\n'),('Website/html/radiomodule.php','Unknown'),('Website/html/reload.php',' 1.0\n'),('Website/html/services.php',' 1.0\n'),('Website/html/statistics.php',' 1.0\n'),('Website/html/stats_popup_day.php',' 1.0\n'),('Website/html/stats_popup_month.php',' 1.0 \n'),('Website/html/stats_popup_week.php',' 1.0\n'),('Website/html/testbuttons.php',' 1.0\n'),('Website/html/timer.php',' 1.0\n'),('Website/html/timer_update.php',' 1.0\n'),('Website/html/update.php',' 1.0\n'),('Website/html/updateSoftware.php',' 1.1\n'),('Website/html/updateVersionDB.php',' 1.0\n'),('Website/html/update_actions.php',' 2.5\n'),('Website/html/version.php',' 1.91\n'),('Website/html/wizard.php',' 1\n'),('Website/html/wrap/wrap_devices.php',' 1.1\n'),('Website/html/wrap/wrap_monitor.php',' 1.1\n'),('Website/html/wrap/wrap_outputs.php',' 1.1\n'),('Website/html/wrap/wrap_owntracks_action.php',' 1.1\n'),('Website/html/wrap/wrap_owntracks_groups.php',' 1.1\n'),('Website/html/wrap/wrap_owntracks_waypoints.php',' 1.1\n'),('Website/html/wrap/wrap_PlayList.php',' 1.1\n'),('Website/html/wrap/wrap_radio.php',' 1.1\n'),('Website/html/wrap/wrap_radiozender.php',' 1.1\n'),('Website/html/wrap/wrap_settings.php',' 1.1\n'),('Website/html/wrap/wrap_vButton.php',' 1.1\n'),('Website/html/wrap/wrap_vButton_actions.php',' 1.1\n'),('Website/html/wrap/wrap_verdiepen.php',' 1.1\n');
/*!40000 ALTER TABLE `html_versions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-14  8:16:56
