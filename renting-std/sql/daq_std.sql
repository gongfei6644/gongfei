/*
Navicat MySQL Data Transfer

Source Server         : daq-std-07
Source Server Version : 50722
Source Host           : 192.168.2.56:3306
Source Database       : daq_std

Target Server Type    : MYSQL
Target Server Version : 50722
File Encoding         : 65001

Date: 2018-12-21 10:32:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `sys_distinct_comparision`
-- ----------------------------
DROP TABLE IF EXISTS `sys_comparision`;
CREATE TABLE `sys_comparision` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `type` int(11) NOT NULL COMMENT '类型：城市-1；区域-2',
  `net_name` varchar(50) NOT NULL COMMENT '网站抓取名',
  `sys_id` int(11) DEFAULT NULL COMMENT '系统区域ID',
  `sys_name` varchar(50) NOT NULL COMMENT '系统区域名',
  `creator` varchar(50) NOT NULL DEFAULT 'SYS',
  `crt_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `modifier` varchar(50) DEFAULT NULL,
  `mod_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `remark` varchar(1000) DEFAULT NULL COMMENT '备注',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '是否有效：0无效，1有效',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of sys_distinct_comparision
-- ----------------------------
INSERT INTO `sys_distinct_comparision` VALUES ('1', '1', '天京市', '3', '天津市', 'SYS', '2018-12-20 19:20:22', null, '2018-12-20 19:20:22', null, '1');


-- ----------------------------
-- Table structure for `dat_unitprice_range`
-- ----------------------------
DROP TABLE IF EXISTS `dat_unitprice_range`;
CREATE TABLE `dat_unitprice_range` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `city_name` varchar(50) NOT NULL COMMENT '城市名称',
  `unitprice_range` varchar(20) NOT NULL COMMENT '单价区间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;