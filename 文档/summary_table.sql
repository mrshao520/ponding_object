/*
 Navicat Premium Data Transfer

 Source Server         : water_sql
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3306
 Source Schema         : water_database

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 04/06/2024 17:32:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for summary_table
-- ----------------------------
DROP TABLE IF EXISTS `summary_table`;
CREATE TABLE `summary_table`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `city` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `description` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `volume` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 90 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
