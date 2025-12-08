CREATE DATABASE  IF NOT EXISTS `sistema_tcc` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sistema_tcc`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: sistema_tcc
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `agendamento_entrega`
--

DROP TABLE IF EXISTS `agendamento_entrega`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agendamento_entrega` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `endereco` text NOT NULL,
  `data_prevista` timestamp NOT NULL,
  `motorista` varchar(255) DEFAULT NULL,
  `veiculo` varchar(255) DEFAULT NULL,
  `observacao` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `pedido_id` (`pedido_id`),
  CONSTRAINT `agendamento_entrega_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agendamento_entrega`
--

LOCK TABLES `agendamento_entrega` WRITE;
/*!40000 ALTER TABLE `agendamento_entrega` DISABLE KEYS */;
/*!40000 ALTER TABLE `agendamento_entrega` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `anexo_pedido`
--

DROP TABLE IF EXISTS `anexo_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anexo_pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `arquivo_url` text NOT NULL,
  `tipo` varchar(100) DEFAULT NULL,
  `enviado_em` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `enviado_por` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `anexo_pedido_ibfk_1` (`pedido_id`),
  KEY `anexo_pedido_ibfk_2` (`enviado_por`),
  CONSTRAINT `anexo_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`) ON DELETE CASCADE,
  CONSTRAINT `anexo_pedido_ibfk_2` FOREIGN KEY (`enviado_por`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anexo_pedido`
--

LOCK TABLES `anexo_pedido` WRITE;
/*!40000 ALTER TABLE `anexo_pedido` DISABLE KEYS */;
/*!40000 ALTER TABLE `anexo_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_clientes` int NOT NULL AUTO_INCREMENT,
  `id_endereco` int NOT NULL,
  `nome` varchar(90) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(110) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `cpf_cnpj` varchar(18) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_clientes`),
  KEY `cliente/endereco_idx` (`id_endereco`),
  CONSTRAINT `cliente/endereco` FOREIGN KEY (`id_endereco`) REFERENCES `endereco` (`id_endereco`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,1,'Murilo Moedas','murilo@gmail.com','12345','309.558.228-10','2025-12-01 16:28:36','2025-12-01 16:28:36');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `endereco`
--

DROP TABLE IF EXISTS `endereco`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `endereco` (
  `id_endereco` int NOT NULL AUTO_INCREMENT,
  `cep` varchar(9) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rua` varchar(105) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `bairro` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cidade` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `estado` varchar(2) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `complemento` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_endereco`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `endereco`
--

LOCK TABLES `endereco` WRITE;
/*!40000 ALTER TABLE `endereco` DISABLE KEYS */;
INSERT INTO `endereco` VALUES (1,'03938-160','Rua Sonata Aurora','Jardim Paraguaçu','272','São Paulo','SP',NULL);
/*!40000 ALTER TABLE `endereco` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoque`
--

DROP TABLE IF EXISTS `estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoque` (
  `id` int NOT NULL AUTO_INCREMENT,
  `variante_id` int NOT NULL,
  `quantidade` int NOT NULL DEFAULT '0',
  `minimo` int NOT NULL DEFAULT '0',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `variante_id` (`variante_id`),
  CONSTRAINT `estoque_ibfk_1` FOREIGN KEY (`variante_id`) REFERENCES `variante` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque`
--

LOCK TABLES `estoque` WRITE;
/*!40000 ALTER TABLE `estoque` DISABLE KEYS */;
INSERT INTO `estoque` VALUES (1,1,0,0,'2025-11-18 14:34:50'),(2,2,0,0,'2025-11-18 14:35:16'),(3,3,0,0,'2025-11-18 14:35:00'),(4,4,0,0,'2025-11-18 19:23:48'),(5,5,0,0,'2025-11-18 19:15:57'),(6,6,0,0,'2025-11-18 20:23:50'),(7,7,5,0,'2025-12-01 15:42:56');
/*!40000 ALTER TABLE `estoque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fase_op`
--

DROP TABLE IF EXISTS `fase_op`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fase_op` (
  `id` int NOT NULL AUTO_INCREMENT,
  `op_id` int NOT NULL,
  `nome` varchar(255) NOT NULL,
  `status` enum('pendente','em_execucao','concluida') DEFAULT 'pendente',
  `inicio` timestamp NULL DEFAULT NULL,
  `fim` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fase_op_ibfk_1` (`op_id`),
  CONSTRAINT `fase_op_ibfk_1` FOREIGN KEY (`op_id`) REFERENCES `op_producao` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fase_op`
--

LOCK TABLES `fase_op` WRITE;
/*!40000 ALTER TABLE `fase_op` DISABLE KEYS */;
/*!40000 ALTER TABLE `fase_op` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `variante_id` int NOT NULL,
  `material` varchar(255) NOT NULL,
  `quantidade` decimal(10,3) NOT NULL,
  `custo_unitario` decimal(12,2) NOT NULL DEFAULT '0.00',
  `unidade_medida` varchar(50) DEFAULT 'un',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_insumos_variante` (`variante_id`),
  CONSTRAINT `fk_insumos_variante` FOREIGN KEY (`variante_id`) REFERENCES `variante` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
INSERT INTO `insumos` VALUES (1,7,'vidro 4mm',1.000,50.00,'un','2025-12-01 15:42:56','2025-12-01 15:42:56'),(2,7,'plastico',1.000,10.00,'m','2025-12-01 15:42:56','2025-12-01 15:42:56');
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_pedido`
--

DROP TABLE IF EXISTS `item_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `variante_id` int NOT NULL,
  `quantidade` int NOT NULL,
  `preco_unit` decimal(12,2) NOT NULL,
  `valor_total` decimal(12,2) NOT NULL,
  `observacoes` text,
  PRIMARY KEY (`id`),
  KEY `item_pedido_ibfk_1` (`pedido_id`),
  KEY `item_pedido_ibfk_2` (`variante_id`),
  CONSTRAINT `item_pedido_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`) ON DELETE CASCADE,
  CONSTRAINT `item_pedido_ibfk_2` FOREIGN KEY (`variante_id`) REFERENCES `variante` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_pedido`
--

LOCK TABLES `item_pedido` WRITE;
/*!40000 ALTER TABLE `item_pedido` DISABLE KEYS */;
INSERT INTO `item_pedido` VALUES (19,19,6,35,150.00,5250.00,NULL),(20,20,6,5,150.00,750.00,NULL);
/*!40000 ALTER TABLE `item_pedido` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tr_item_pedido_valor_total` BEFORE INSERT ON `item_pedido` FOR EACH ROW BEGIN
  SET NEW.valor_total = NEW.preco_unit * NEW.quantidade;
END */;;
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
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tr_item_pedido_valor_total_update` BEFORE UPDATE ON `item_pedido` FOR EACH ROW BEGIN
  SET NEW.valor_total = NEW.preco_unit * NEW.quantidade;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `movimento_estoque`
--

DROP TABLE IF EXISTS `movimento_estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimento_estoque` (
  `id` int NOT NULL AUTO_INCREMENT,
  `estoque_id` int NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `quantidade` int NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `data` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `observacao` text,
  PRIMARY KEY (`id`),
  KEY `movimento_estoque_ibfk_1` (`estoque_id`),
  KEY `movimento_estoque_ibfk_2` (`usuario_id`),
  CONSTRAINT `movimento_estoque_ibfk_1` FOREIGN KEY (`estoque_id`) REFERENCES `estoque` (`id`),
  CONSTRAINT `movimento_estoque_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimento_estoque`
--

LOCK TABLES `movimento_estoque` WRITE;
/*!40000 ALTER TABLE `movimento_estoque` DISABLE KEYS */;
INSERT INTO `movimento_estoque` VALUES (1,1,1,5,'Entrada manual','2025-11-17 18:47:41',NULL),(2,1,1,5,'Entrada manual','2025-11-17 18:47:45',NULL),(3,1,1,5,'Entrada manual','2025-11-17 18:47:52',NULL),(4,2,2,-5,'Venda','2025-11-17 19:27:21',NULL),(5,1,1,-10,'Venda','2025-11-17 19:29:53',NULL),(6,1,1,5,'Venda','2025-11-17 19:49:54',NULL),(7,2,1,5,'Entrada manual','2025-11-17 19:50:20',NULL),(8,2,2,5,'Venda','2025-11-17 19:52:31',NULL),(9,2,1,5,'Venda','2025-11-17 19:52:49',NULL),(10,2,1,1,'Entrada manual','2025-11-17 20:02:21',NULL),(11,2,1,1,'Entrada manual','2025-11-17 20:02:44',NULL),(12,3,2,150,'Venda','2025-11-17 21:32:40',NULL),(13,3,1,300,'Venda','2025-11-17 21:39:42',NULL),(14,1,1,5,'Venda','2025-11-17 21:40:28',NULL),(15,3,1,250,'Venda','2025-11-17 22:02:07',NULL),(16,1,1,6,'Venda','2025-11-17 22:12:26',NULL),(17,1,2,10,'Venda','2025-11-17 22:15:18',NULL),(18,2,1,5,'Venda','2025-11-17 22:18:35',NULL),(19,3,1,150,'Venda','2025-11-17 22:24:08',NULL),(20,3,1,150,'Venda Pedido #17','2025-11-18 14:23:08',NULL);
/*!40000 ALTER TABLE `movimento_estoque` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tr_movimento_estoque` AFTER INSERT ON `movimento_estoque` FOR EACH ROW BEGIN
  UPDATE estoque
  SET quantidade = quantidade + NEW.quantidade
  WHERE id = NEW.estoque_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `op_producao`
--

DROP TABLE IF EXISTS `op_producao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `op_producao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_pedido_id` int NOT NULL,
  `status` enum('aberto','em_andamento','concluido') DEFAULT 'aberto',
  `data_abertura` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `data_conclusao` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_pedido_id` (`item_pedido_id`),
  CONSTRAINT `op_producao_ibfk_1` FOREIGN KEY (`item_pedido_id`) REFERENCES `item_pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `op_producao`
--

LOCK TABLES `op_producao` WRITE;
/*!40000 ALTER TABLE `op_producao` DISABLE KEYS */;
/*!40000 ALTER TABLE `op_producao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cliente_nome` varchar(255) NOT NULL,
  `cliente_contato` varchar(255) DEFAULT NULL,
  `status` enum('criado','aprovado','em_producao','em_logistica','entregue','finalizado') DEFAULT 'criado',
  `total` decimal(14,2) NOT NULL DEFAULT '0.00',
  `criado_por` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `pedido_ibfk_1` (`criado_por`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`criado_por`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (19,'Cliente ID 1',NULL,'criado',5250.00,1,'2025-11-18 20:11:04','2025-11-18 20:11:04'),(20,'henzo',NULL,'criado',750.00,1,'2025-11-18 20:23:08','2025-11-18 20:23:08');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produto`
--

DROP TABLE IF EXISTS `produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `linha` varchar(255) NOT NULL,
  `formato` varchar(255) NOT NULL,
  `descricao` text,
  `imagem_url` text,
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto`
--

LOCK TABLES `produto` WRITE;
/*!40000 ALTER TABLE `produto` DISABLE KEYS */;
INSERT INTO `produto` VALUES (1,'espelho grande','redondo','espelho redondo grande','',1,'2025-11-17 18:44:00','2025-11-17 18:44:00'),(2,'espelho grande','quadrado','sim','',1,'2025-11-17 18:46:48','2025-11-17 18:46:48'),(3,'espelho grande','losango','é um espelho','',1,'2025-11-17 18:55:42','2025-11-17 18:55:42'),(4,'espelho grande','losango','é um espelho','',1,'2025-11-17 20:13:46','2025-11-17 20:13:46'),(5,'espelho prime','retangular','espelho safado','',1,'2025-11-18 16:52:47','2025-11-18 16:52:47'),(6,'espelho','retangular','sim','',1,'2025-11-18 19:12:55','2025-11-18 19:12:55'),(7,'espelho','redondo','sim','',1,'2025-11-18 19:29:52','2025-11-18 19:29:52'),(8,'Espelho','redondo','espelho redondo com moldura de aluminio',NULL,1,'2025-12-01 15:42:56','2025-12-01 15:42:56');
/*!40000 ALTER TABLE `produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessao`
--

DROP TABLE IF EXISTS `sessao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessao` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `user_agent` text,
  `criado_em` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `expiracao` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sessao_ibfk_1` (`usuario_id`),
  CONSTRAINT `sessao_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessao`
--

LOCK TABLES `sessao` WRITE;
/*!40000 ALTER TABLE `sessao` DISABLE KEYS */;
/*!40000 ALTER TABLE `sessao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tracking`
--

DROP TABLE IF EXISTS `tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tracking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `evento` enum('roteirizado','em_rota','entregue') NOT NULL,
  `detalhes` text,
  `data` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `foto_url` text,
  PRIMARY KEY (`id`),
  KEY `tracking_ibfk_1` (`pedido_id`),
  CONSTRAINT `tracking_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tracking`
--

LOCK TABLES `tracking` WRITE;
/*!40000 ALTER TABLE `tracking` DISABLE KEYS */;
/*!40000 ALTER TABLE `tracking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `senha_hash` text NOT NULL,
  `perfil` varchar(50) DEFAULT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  `criado_em` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'henzo','henzo@gmail.com','scrypt:32768:8:1$GiQ87ZPnM8u4bTlm$60b3c55ce49714d62c23b0f2ccc307da651b78f2d2261c856e018a05e55d9284bd49042ed19fb02314dd3e888e4a368bec6022081e9a5e11b7d72e623d113377','cliente',1,'2025-11-03 14:47:54','2025-11-03 11:47:53'),(2,'bruno','1@gmail.com','scrypt:32768:8:1$bIpTiikJSTb1yEqp$32c6d907918c5d5abea3d741462c45222776d46ee81a29db53e177cef8b4392c078b6ec71ecfbf7c9c3ec4438d87b01cc35de8f518ef1de5851676cc906fc8f1','cliente',1,'2025-11-03 15:05:33','2025-11-03 12:05:32'),(3,'bruno','bruno@gmail.com','scrypt:32768:8:1$fFnxaDxfYk8PvpjF$7dee3a7a08a38ccb765581d3e7f4df68fbdf252e913df34b572257fb70a7f23a7ebbde4204e2179c6b7f96623e9e45554adcff4814cb13712888102ed187826a','cliente',1,'2025-11-03 17:18:45','2025-11-03 14:18:45'),(4,'inouye','inouye@gmail.com','scrypt:32768:8:1$QXVyedfNNjurFYBg$c1c75c4f08c90139832d5af1bedab2998299f0097e688c0f0edea4b913db286f57944036568d0d118417e5c57ba6f1c5582c2ff650ef8d9039258698c7e6e1cd','cliente',1,'2025-11-18 21:35:55','2025-11-18 21:35:55'),(5,'gustavo','gustavo@gmail.com','scrypt:32768:8:1$UV6wAl3m1LEVKJfH$b806670800c2a959b94c25b874facb8975bde4097c2afd3d17cd823e6979a416d52ea2cd76232aa8b1bffa99730423cded317394c8daf5623bfa5c58ec92022f','cliente',1,'2025-12-01 15:15:16','2025-12-01 15:15:16');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `variante`
--

DROP TABLE IF EXISTS `variante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `variante` (
  `id` int NOT NULL AUTO_INCREMENT,
  `produto_id` int NOT NULL,
  `altura_cm` decimal(7,2) DEFAULT NULL,
  `largura_cm` decimal(7,2) DEFAULT NULL,
  `cor` varchar(100) DEFAULT NULL,
  `led_direto` tinyint(1) NOT NULL DEFAULT '0',
  `led_indireto` tinyint(1) NOT NULL DEFAULT '0',
  `moldura` varchar(100) DEFAULT NULL,
  `sku` varchar(100) NOT NULL,
  `preco_base` decimal(12,2) NOT NULL,
  `ativo` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `variante_ibfk_1` (`produto_id`),
  CONSTRAINT `variante_ibfk_1` FOREIGN KEY (`produto_id`) REFERENCES `produto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variante`
--

LOCK TABLES `variante` WRITE;
/*!40000 ALTER TABLE `variante` DISABLE KEYS */;
INSERT INTO `variante` VALUES (1,2,100.00,150.00,'preto',0,0,'sem','ESP-100-150-PRETO-SEM',150.00,0,'2025-11-17 18:46:48','2025-11-18 14:34:50'),(2,3,100.00,150.00,'branco',1,1,'aluminio','ESP-100-150-BRANCO-ALUM',200.00,0,'2025-11-17 18:55:42','2025-11-18 14:35:16'),(3,4,500.00,300.00,'amarelo',1,0,'metal','ESP-500-300-AMAREL-META',500.00,0,'2025-11-17 20:13:46','2025-11-18 14:35:00'),(4,5,600.00,300.00,'branco',1,1,'metal','ESP-600-300-BRANCO-META',155.00,0,'2025-11-18 16:52:47','2025-11-18 19:23:48'),(5,6,100.00,100.00,'preto',1,0,'metal','ESP-100-100-PRETO-META',150.00,0,'2025-11-18 19:12:55','2025-11-18 19:15:57'),(6,7,100.00,120.00,'preto',1,1,'metal','ESP-100-120-PRETO-META',150.00,0,'2025-11-18 19:29:52','2025-11-18 20:23:50'),(7,8,50.00,50.00,'preto',0,0,'aluminio','ESP-50-50-PRETO-ALUM',68.75,1,'2025-12-01 15:42:56','2025-12-01 15:42:56');
/*!40000 ALTER TABLE `variante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vw_catalogo`
--

DROP TABLE IF EXISTS `vw_catalogo`;
/*!50001 DROP VIEW IF EXISTS `vw_catalogo`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vw_catalogo` AS SELECT 
 1 AS `produto_id`,
 1 AS `variante_id`,
 1 AS `linha`,
 1 AS `formato`,
 1 AS `altura_cm`,
 1 AS `largura_cm`,
 1 AS `cor`,
 1 AS `led_direto`,
 1 AS `led_indireto`,
 1 AS `moldura`,
 1 AS `sku`,
 1 AS `preco_base`,
 1 AS `estoque`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'sistema_tcc'
--

--
-- Dumping routines for database 'sistema_tcc'
--

--
-- Final view structure for view `vw_catalogo`
--

/*!50001 DROP VIEW IF EXISTS `vw_catalogo`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vw_catalogo` AS select `p`.`id` AS `produto_id`,`v`.`id` AS `variante_id`,`p`.`linha` AS `linha`,`p`.`formato` AS `formato`,`v`.`altura_cm` AS `altura_cm`,`v`.`largura_cm` AS `largura_cm`,`v`.`cor` AS `cor`,`v`.`led_direto` AS `led_direto`,`v`.`led_indireto` AS `led_indireto`,`v`.`moldura` AS `moldura`,`v`.`sku` AS `sku`,`v`.`preco_base` AS `preco_base`,`e`.`quantidade` AS `estoque` from ((`produto` `p` join `variante` `v` on((`v`.`produto_id` = `p`.`id`))) left join `estoque` `e` on((`e`.`variante_id` = `v`.`id`))) where ((`p`.`ativo` = 1) and (`v`.`ativo` = 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-01 10:29:16
