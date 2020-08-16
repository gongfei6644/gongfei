/*
Navicat MySQL Data Transfer

Source Server         : 采集平台
Source Server Version : 50505
Source Host           : 192.168.2.60:3306
Source Database       : das-job-prod

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2019-05-08 15:56:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `sys_city_weight`
-- ----------------------------
DROP TABLE IF EXISTS `sys_city_weight`;
CREATE TABLE `sys_city_weight` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city_id` int(11) NOT NULL COMMENT '城市ID',
  `city_name` varchar(30) NOT NULL COMMENT '城市名称',
  `city_level` varchar(30) DEFAULT NULL COMMENT '城市等级',
  `city_weight` int(11) DEFAULT NULL COMMENT '城市权重',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=825 DEFAULT CHARSET=utf8 COMMENT '城市权重表';

update sys_city_weight set city_weight=80 where city_level='一线';
update sys_city_weight set city_weight=50 where city_level='二线';
update sys_city_weight set city_weight=30 where city_level='三线重要';
update sys_city_weight set city_weight=10 where city_level='三线其他';
update sys_city_weight set city_weight=5 where city_level is null;

