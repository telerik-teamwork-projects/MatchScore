-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: telerik-mariadb-server.mariadb.database.azure.com    Database: matchscore_db
-- ------------------------------------------------------
-- Server version	5.6.47.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `director_requests`
--

LOCK TABLES `director_requests` WRITE;
/*!40000 ALTER TABLE `director_requests` DISABLE KEYS */;
INSERT INTO `director_requests` VALUES (1,12,'toni5@example.com','accepted','2023-11-16 16:21:55'),(2,3,'antonioboyanov9test@gmail.com','rejected','2023-11-16 20:16:03'),(3,38,'antonioboyanov9test+test2@gmail.com','accepted','2023-11-23 20:14:12'),(4,44,'director@abv.bg','accepted','2023-11-27 05:09:49');
/*!40000 ALTER TABLE `director_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `link_player_requests`
--

LOCK TABLES `link_player_requests` WRITE;
/*!40000 ALTER TABLE `link_player_requests` DISABLE KEYS */;
INSERT INTO `link_player_requests` VALUES (10,45,'geri_player','Petra Kvitova','accepted','2023-11-28 07:40:12');
/*!40000 ALTER TABLE `link_player_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `matches`
--

LOCK TABLES `matches` WRITE;
/*!40000 ALTER TABLE `matches` DISABLE KEYS */;
INSERT INTO `matches` VALUES (1,'2023-11-01 00:00:00','score',1,NULL,1),(2,'2023-11-01 00:00:00','score',1,NULL,1),(3,'2023-11-01 00:00:00','score',1,NULL,1),(4,'2023-11-02 00:00:00','score',1,NULL,2),(5,'2023-11-02 00:00:00','score',1,NULL,2),(6,'2023-11-02 00:00:00','score',1,NULL,2),(7,'2023-11-03 00:00:00','score',1,NULL,3),(8,'2023-11-03 00:00:00','score',1,NULL,3),(9,'2023-11-03 00:00:00','score',1,NULL,3),(10,'2023-11-04 00:00:00','score',1,NULL,4),(11,'2023-11-04 00:00:00','score',1,NULL,4),(12,'2023-11-04 00:00:00','score',1,NULL,4),(13,'2023-11-05 00:00:00','score',1,NULL,5),(14,'2023-11-05 00:00:00','score',1,NULL,5),(15,'2023-11-05 00:00:00','score',1,NULL,5),(16,'2023-11-20 00:00:00','score',2,20,1),(17,'2023-11-20 00:00:00','score',2,20,1),(18,'2023-11-20 00:00:00','score',2,21,1),(19,'2023-11-20 00:00:00','score',2,21,1),(20,'2023-11-21 00:00:00','score',2,22,2),(21,'2023-11-21 00:00:00','score',2,22,2),(22,'2023-11-22 00:00:00','score',2,NULL,3),(23,'2023-11-23 00:00:00','score',2,NULL,4),(24,'2023-12-06 00:00:00','score',3,NULL,1),(25,'2023-12-06 00:00:00','score',3,NULL,1),(26,'2023-12-07 00:00:00','score',3,NULL,2),(27,'2023-12-07 00:00:00','score',3,NULL,2),(28,'2023-12-08 00:00:00','score',3,NULL,3),(29,'2023-12-08 00:00:00','score',3,NULL,3),(30,'2023-12-04 00:00:00','time',5,NULL,1),(31,'2023-12-04 00:00:00','time',5,NULL,1),(32,'2023-12-05 00:00:00','time',5,NULL,2),(33,'2023-12-05 00:00:00','time',5,NULL,2),(34,'2023-12-06 00:00:00','time',5,NULL,3),(35,'2023-12-06 00:00:00','time',5,NULL,3),(36,'2023-12-03 00:00:00','score',6,38,1),(37,'2023-12-03 00:00:00','score',6,38,1),(38,'2023-12-04 00:00:00','score',6,NULL,2),(39,'2023-12-06 00:00:00','score',4,43,1),(40,'2023-12-06 00:00:00','score',4,43,1),(41,'2023-12-06 00:00:00','score',4,44,1),(42,'2023-12-06 00:00:00','score',4,44,1),(43,'2023-12-07 00:00:00','score',4,45,2),(44,'2023-12-07 00:00:00','score',4,45,2),(45,'2023-12-08 00:00:00','score',4,NULL,3),(46,'2023-12-09 00:00:00','score',4,NULL,4),(47,'2023-12-07 00:00:00','time',7,NULL,1),(48,'2023-12-07 00:00:00','time',7,NULL,1),(49,'2023-12-08 00:00:00','time',7,NULL,2),(50,'2023-12-08 00:00:00','time',7,NULL,2),(51,'2023-12-09 00:00:00','time',7,NULL,3),(52,'2023-12-09 00:00:00','time',7,NULL,3),(53,'2023-12-07 00:00:00','score',8,55,1),(54,'2023-12-07 00:00:00','score',8,55,1),(55,'2023-12-08 00:00:00','score',8,NULL,2);
/*!40000 ALTER TABLE `matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `players`
--

LOCK TABLES `players` WRITE;
/*!40000 ALTER TABLE `players` DISABLE KEYS */;
INSERT INTO `players` VALUES (1,'Coco Gauff','UNITED STATES ',NULL,'/media/players_pics/eac86097-2e78-4d26-a59a-4fab6f3b45f0_coco.jpg',NULL),(2,'Maria Sakkari',NULL,NULL,NULL,NULL),(3,'Petra Kvitova','CZECH REPUBLIC',NULL,'/media/players_pics/09ca6678-64aa-49ad-8202-5cccd6e96a84_kvitova.jpg',45),(5,'Qinwen Zheng',NULL,NULL,NULL,11),(7,'Jelena Ostapenko',NULL,NULL,NULL,NULL),(9,'Belinda Bencic',NULL,NULL,NULL,NULL),(10,'Victoria Azarenka','BELARUS',NULL,'/media/players_pics/8936e4d5-4cb5-4827-b90f-1660c467a30d_azarenka.jpg',NULL),(11,'Serena Williams',NULL,NULL,NULL,NULL),(12,'Laura Siegemund',NULL,NULL,NULL,NULL),(13,'Caroline Wozniacki','DENMARK',NULL,'/media/players_pics/16efaeaf-2752-4519-9ca5-7fb0811dfd60_Wozniacki.jpg',NULL),(15,'Angelique Kerber','GERMANY',NULL,'/media/players_pics/91120c80-4c6e-4dc6-9649-99b0a54c0acc_Kerber.jpg',NULL),(16,'Iga Swiatek','POLAND',NULL,'/media/players_pics/84d85677-32a8-47c7-a443-62dc428717bb_swiatek.jpg',NULL),(23,'Aryna Sabalenka','BELARUS',NULL,'/media/players_pics/b5685129-737b-4d6a-a21f-c1bcbf388907_sablenka.jpg',NULL),(32,'Elisabetta Cocciaretto',NULL,NULL,NULL,NULL),(40,'Simona Halep','ROMANIA','',NULL,46),(45,'Peter Petrov','Bulgaria','Lokomotiv',NULL,55);
/*!40000 ALTER TABLE `players` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `players_matches`
--

LOCK TABLES `players_matches` WRITE;
/*!40000 ALTER TABLE `players_matches` DISABLE KEYS */;
INSERT INTO `players_matches` VALUES (1,17,3,2),(1,20,1,0),(1,23,1,0),(1,48,0,0),(1,49,0,0),(1,52,0,0),(2,18,0,0),(2,42,0,0),(3,3,2,1),(3,6,2,2),(3,8,0,0),(3,10,0,0),(3,14,2,2),(3,16,2,2),(3,20,2,2),(3,22,1,0),(3,36,1,2),(3,38,1,0),(3,39,0,0),(3,47,0,0),(3,49,0,0),(3,51,0,0),(3,53,0,0),(7,36,0,0),(7,42,0,0),(9,19,1,0),(9,25,0,0),(9,26,0,0),(9,29,0,0),(9,30,0,0),(9,32,0,0),(9,34,0,0),(9,41,0,0),(9,54,0,0),(10,3,2,1),(10,5,2,2),(10,7,1,0),(10,11,2,2),(10,15,2,0),(11,30,0,0),(11,33,0,0),(11,35,0,0),(11,37,2,2),(11,38,3,2),(12,31,0,0),(12,33,0,0),(12,34,0,0),(12,47,0,0),(12,50,0,0),(12,52,0,0),(13,1,2,2),(13,4,1,0),(13,7,2,2),(13,10,2,2),(13,13,2,2),(13,19,2,2),(13,21,0,0),(13,23,2,2),(13,24,1,2),(13,26,0,0),(13,28,0,0),(13,31,0,0),(13,32,0,0),(13,35,0,0),(13,40,0,0),(13,54,0,0),(15,1,1,0),(15,5,1,0),(15,9,1,1),(15,12,0,0),(15,14,1,0),(16,2,2,2),(16,4,2,2),(16,8,2,2),(16,12,2,2),(16,15,3,2),(16,18,2,2),(16,21,2,2),(16,22,3,2),(16,37,1,0),(16,48,0,0),(16,50,0,0),(16,51,0,0),(23,2,1,0),(23,6,1,0),(23,9,1,1),(23,11,1,0),(23,13,0,0),(23,17,1,0),(23,24,0,0),(23,27,0,0),(23,29,0,0),(23,41,0,0),(23,53,0,0),(32,16,1,0),(32,25,0,0),(32,27,0,0),(32,28,0,0),(32,39,0,0),(40,40,0,0);
/*!40000 ALTER TABLE `players_matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `players_requests`
--

LOCK TABLES `players_requests` WRITE;
/*!40000 ALTER TABLE `players_requests` DISABLE KEYS */;
INSERT INTO `players_requests` VALUES (8,46,'Simona Halep','ROMANIA','','accepted'),(15,55,'Peter Petrov','Bulgaria','Lokomotiv','accepted');
/*!40000 ALTER TABLE `players_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `players_tournaments`
--

LOCK TABLES `players_tournaments` WRITE;
/*!40000 ALTER TABLE `players_tournaments` DISABLE KEYS */;
INSERT INTO `players_tournaments` VALUES (1,2,0),(1,7,0),(2,2,0),(2,4,0),(3,1,0),(3,2,0),(3,4,0),(3,6,0),(3,7,0),(3,8,0),(7,4,0),(7,6,0),(9,2,0),(9,3,0),(9,4,0),(9,5,0),(9,8,0),(10,1,0),(11,5,0),(11,6,1),(12,5,0),(12,7,0),(13,1,0),(13,2,0),(13,3,0),(13,4,0),(13,5,0),(13,8,0),(15,1,0),(16,1,1),(16,2,1),(16,6,0),(16,7,0),(23,1,0),(23,2,0),(23,3,0),(23,4,0),(23,8,0),(32,2,0),(32,3,0),(32,4,0),(40,4,0);
/*!40000 ALTER TABLE `players_tournaments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `players_tournaments_prizes`
--

LOCK TABLES `players_tournaments_prizes` WRITE;
/*!40000 ALTER TABLE `players_tournaments_prizes` DISABLE KEYS */;
/*!40000 ALTER TABLE `players_tournaments_prizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `requests`
--

LOCK TABLES `requests` WRITE;
/*!40000 ALTER TABLE `requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `tournament_requests`
--

LOCK TABLES `tournament_requests` WRITE;
/*!40000 ALTER TABLE `tournament_requests` DISABLE KEYS */;
INSERT INTO `tournament_requests` VALUES (1,40,4,NULL,'Simona Halep','ROMANIA','','accepted','2023-12-05 14:04:24'),(2,3,4,NULL,'Petra Kvitova','CZECH REPUBLIC',NULL,'accepted','2023-12-05 14:13:30'),(3,3,8,NULL,'Petra Kvitova','CZECH REPUBLIC',NULL,'accepted','2023-12-06 10:43:34');
/*!40000 ALTER TABLE `tournament_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `tournaments`
--

LOCK TABLES `tournaments` WRITE;
/*!40000 ALTER TABLE `tournaments` DISABLE KEYS */;
INSERT INTO `tournaments` VALUES (1,'league','WTA League Sofia','WTA Singles League','score',5,0,'closed','Sofia, Bulgaria','2023-11-01 00:00:00','2023-11-05 00:00:00',1),(2,'knockout','MundoTenis Open','Top 3 KnockOut','score',4,1,'closed','Florianopolis, Brazil','2023-11-20 00:00:00','2023-11-23 00:00:00',1),(3,'league','United Cup','WTA Singles League','score',3,0,'closed','Sydney, Australia','2023-12-06 00:00:00','2023-12-08 00:00:00',44),(4,'knockout','Open Angers Arena','Top 3 KnockOut','score',4,1,'closed','Angers, France','2023-12-06 00:00:00','2023-12-09 00:00:00',44),(5,'league','Varna Open League','WTA Singles League','time',3,0,'closed','Varna, Bulgaria','2023-12-04 00:00:00','2023-12-06 00:00:00',44),(6,'knockout','Montevideo Open','Top 2 KnockOut','score',2,0,'closed','Montevideo, Uruguay','2023-12-03 00:00:00','2023-12-04 00:00:00',44),(7,'league','Plovdiv Open','test','time',3,0,'closed','Plovdiv, Bulgaria','2023-12-07 00:00:00','2023-12-09 00:00:00',44),(8,'knockout','Shumen Open','','score',2,0,'closed','Shumen, Bulgaria','2023-12-07 00:00:00','2023-12-08 00:00:00',44);
/*!40000 ALTER TABLE `tournaments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `tournaments_prizes`
--

LOCK TABLES `tournaments_prizes` WRITE;
/*!40000 ALTER TABLE `tournaments_prizes` DISABLE KEYS */;
/*!40000 ALTER TABLE `tournaments_prizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'geri_admin','admin@abv.bg','$2b$12$uMuKOMl4IThBZ29fJL1/D.bOtZtPwfmsprPdWw/eS2/jEb48Zal.O','admin',NULL,'/media/profile_pics/e271fb9a-5c53-4102-9a99-74ebd8345ab8_test_pic2.jpg','/media/cover_pics/8dc48708-1404-4ea4-98cc-1875d21d2228_fon.jpg'),(3,'aboyanov9','antonioboyanov9test@gmail.com','$2b$12$we.sqHz222TnQulCo5BXEOMnq4A0m9bdjlPs9c6GAFDsKnBc9.wfy','admin','This profile is admin. Feel free to ask if you have any questions.','/media/profile_pics/e34f82bc-9a6e-44ba-a781-00953f29db2b_cv_photo.jpg','/media/cover_pics/9f3a8cbe-c9cd-4169-90ac-05cddcae6874_levski.png'),(4,'toni','toni@example.com','$2b$12$378L5qNL.S/RxPpT2sv90ORabEwfAri56u2Vo1X2yo0zeTseMEMyy','user',NULL,NULL,NULL),(5,'toni2','toni2@example.com','$2b$12$vBm.fnrIx7MpE7ew/MhOrOEGCEHW8eSjYwQoRCWpVHfE.iycZ0QRi','user',NULL,NULL,NULL),(9,'toni6','toni6@example.com','$2b$12$W6P9XOQICZF8zcvTcWGhUewoTGoqB5y3ecXw.AEdWUvFk.smjL/LK','user','I like Tennis','/media/profile_pics/93aca402-c38a-4474-b1e6-d8fbe5a3769a_profile-pic.jpg',''),(10,'toni3','toni3@example.com','$2b$12$iPiNYh1KOl353JS34qPce.Jd0kTa8CzOQ/PN4/C3N2LO9hEAmLO5u','user',NULL,NULL,NULL),(11,'toni4','toni4@example.com','$2b$12$KEou5JEY1s8wzXZDbqt8IehRojdBPCgbEz0X75Robi2ye/yZ.axtu','user',NULL,NULL,NULL),(12,'toni5','toni5@example.com','$2b$12$8.A4WiEDGTBHg5oYQ43EOuEzRlfx917hhMhsFMtGwe.X.ib8qZdUy','director',NULL,'/media/profile_pics/6b83f7b7-2ec8-45cb-9e48-2ae137b50c60_profile-pic.jpg',''),(13,'toni7','toni7@gmail.com','$2b$12$nawoZksy0Kli/DfnGVV78.a1Idgqz1shxC0UvtfnEyAo1xNPFFH92','user',NULL,NULL,NULL),(14,'Toni18','toni18@example.com','$2b$12$i0jAdZqHVLTLZ0rxDatbh.EaihOPrqU2i/V/7rhtPdnpLfg3.Fx2q','user',NULL,NULL,NULL),(15,'Grigor Dimitrov','grigordimitrov@example.com','$2b$12$Y8kQR4jY.30.3NCZLrzUx.XcVRTHkjZsNmOln34H5/mavw6u3g0Xi','user',NULL,NULL,NULL),(16,'FootballFan','antonioboyanov9test+test1@gmail.com','$2b$12$l504wx1lI5nvcAbAVtHD1uDzkoB9RYJoYsd2fOe7fvqwAl1PSiPVS','user',NULL,NULL,NULL),(33,'peter82','antonioboyanov9test+test7@gmail.com','$2b$12$Goje3yLaO6VEeSiluWvZg.6/RGCOHPZJko.X6TgbuSfuynzeVIC6e','user',NULL,NULL,NULL),(34,'peter72','antonioboyanov9test+test8@gmail.com','$2b$12$leCulnoLAVV0yuUi3TDiJuJCID8hIu4GZTy1WcFaeEbbQnEfjCIre','user',NULL,NULL,NULL),(35,'peter12','antonioboyanov9test+test9@gmail.com','$2b$12$8ayeoQGA2cB29JL5VrNi5un83f646OTgoe7Neappon6vzhRXpeScG','user',NULL,NULL,NULL),(36,'gosahui21','antonioboyanov9test+test10@gmail.com','$2b$12$AD148jHRj9KjA48xLRv1Iu1YGrcX8xmrpNcWVgrosx5U8xfWMaDou','user',NULL,NULL,NULL),(37,'fdhiu832','antonioboyanov9test+test11@gmail.com','$2b$12$veGIkJdmRPtpkPG2amMhnO6elFAS.bm81WsO4fwnyKeAFP8JLLRLC','user',NULL,NULL,NULL),(38,'codingMaster123','antonioboyanov9test+test2@gmail.com','$2b$12$I0QTISza4OCrPRBjtqnoXuwebmAk0U..tIP5t9i/0S3eWi92avu7y','director',NULL,NULL,NULL),(39,'superMario','antonioboyanov9test+test15@gmail.com','$2b$12$.pCKLOxmazWl0r/GgAS4I.t6l5VWPFRCo/LnqGjb0CAEgNC7BKbPa','user',NULL,NULL,NULL),(41,'ballingBad','antonioboyanov9test+test14@gmail.com','$2b$12$X1QC6p26qGvRjdUf6VlbNuPGk8dOEp.5i82aKA/AVixSK0/j91P1K','user',NULL,NULL,NULL),(42,'soccerPlayer','antonioboyanov9test+test13@gmail.com','$2b$12$rHfa2D0xBNRkhSAJQwncEe.KXrk7N8QVN2X2fOjvW7OAZV26AQJq6','user',NULL,NULL,NULL),(43,'mariaG12','antonioboyanov9test+test12@gmail.com','$2b$12$uAm919AUMTKphA4IRJJhBeGm8EJjPszZMivbkBAFThHw.WGcT6/me','user',NULL,NULL,NULL),(44,'geri_director','director@abv.bg','$2b$12$erJ4NB7qwcKDYlEBY3AuEO4fw93DA90pmZcfp2vTK3F.MdoYGOnXy','director',NULL,NULL,NULL),(45,'geri_player','info.matchscore+test1@gmail.com','$2b$12$9OTfaqzMEnlkVAUX2KRAEe7PeDYdiV/Ex/72T7NJ0kZUp2Z5acx0.','user',NULL,NULL,NULL),(46,'Poul','user@abv.bg','$2b$12$9itiGeBirvbE29BDPIELgucz1qepeodOYHBiltrG9wTk5PuN790jO','user',NULL,NULL,NULL),(55,'testUser','antonioboyanov9test+test3@gmail.com','$2b$12$9l37UsebJj4rH8OO4FsIR.t8RzAhICVRLC7c4s44.C8pv7sNCUv6i','user',NULL,'/media/profile_pics/4b4f3701-326c-4d0f-b1a4-4e8f828cb43a_demo_img.jpg','');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-06 18:24:28
