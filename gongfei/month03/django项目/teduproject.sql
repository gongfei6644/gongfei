/*
 Navicat Premium Data Transfer

 Source Server         : new
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : mxonline

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 13/06/2019 11:29:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
INSERT INTO `auth_group` VALUES (1, '编辑部门');

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
INSERT INTO `auth_group_permissions` VALUES (2, 1, 37);
INSERT INTO `auth_group_permissions` VALUES (3, 1, 38);
INSERT INTO `auth_group_permissions` VALUES (5, 1, 46);
INSERT INTO `auth_group_permissions` VALUES (6, 1, 47);
INSERT INTO `auth_group_permissions` VALUES (1, 1, 68);
INSERT INTO `auth_group_permissions` VALUES (4, 1, 69);

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 108 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (5, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (8, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (9, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (17, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (18, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (19, 'Can add 用户信息', 7, 'add_userprofile');
INSERT INTO `auth_permission` VALUES (20, 'Can change 用户信息', 7, 'change_userprofile');
INSERT INTO `auth_permission` VALUES (21, 'Can delete 用户信息', 7, 'delete_userprofile');
INSERT INTO `auth_permission` VALUES (22, 'Can add 邮箱验证码', 8, 'add_emailverifyrecord');
INSERT INTO `auth_permission` VALUES (23, 'Can change 邮箱验证码', 8, 'change_emailverifyrecord');
INSERT INTO `auth_permission` VALUES (24, 'Can delete 邮箱验证码', 8, 'delete_emailverifyrecord');
INSERT INTO `auth_permission` VALUES (25, 'Can add 轮播图', 9, 'add_banner');
INSERT INTO `auth_permission` VALUES (26, 'Can change 轮播图', 9, 'change_banner');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 轮播图', 9, 'delete_banner');
INSERT INTO `auth_permission` VALUES (28, 'Can add 城市', 10, 'add_citydict');
INSERT INTO `auth_permission` VALUES (29, 'Can change 城市', 10, 'change_citydict');
INSERT INTO `auth_permission` VALUES (30, 'Can delete 城市', 10, 'delete_citydict');
INSERT INTO `auth_permission` VALUES (31, 'Can add 课程机构', 11, 'add_courseorg');
INSERT INTO `auth_permission` VALUES (32, 'Can change 课程机构', 11, 'change_courseorg');
INSERT INTO `auth_permission` VALUES (33, 'Can delete 课程机构', 11, 'delete_courseorg');
INSERT INTO `auth_permission` VALUES (34, 'Can add 教师', 12, 'add_teacher');
INSERT INTO `auth_permission` VALUES (35, 'Can change 教师', 12, 'change_teacher');
INSERT INTO `auth_permission` VALUES (36, 'Can delete 教师', 12, 'delete_teacher');
INSERT INTO `auth_permission` VALUES (37, 'Can add 课程', 13, 'add_course');
INSERT INTO `auth_permission` VALUES (38, 'Can change 课程', 13, 'change_course');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 课程', 13, 'delete_course');
INSERT INTO `auth_permission` VALUES (40, 'Can add 章节', 14, 'add_lesson');
INSERT INTO `auth_permission` VALUES (41, 'Can change 章节', 14, 'change_lesson');
INSERT INTO `auth_permission` VALUES (42, 'Can delete 章节', 14, 'delete_lesson');
INSERT INTO `auth_permission` VALUES (43, 'Can add 视频', 15, 'add_video');
INSERT INTO `auth_permission` VALUES (44, 'Can change 视频', 15, 'change_video');
INSERT INTO `auth_permission` VALUES (45, 'Can delete 视频', 15, 'delete_video');
INSERT INTO `auth_permission` VALUES (46, 'Can add 课程资源', 16, 'add_coursesource');
INSERT INTO `auth_permission` VALUES (47, 'Can change 课程资源', 16, 'change_coursesource');
INSERT INTO `auth_permission` VALUES (48, 'Can delete 课程资源', 16, 'delete_coursesource');
INSERT INTO `auth_permission` VALUES (49, 'Can add 用户咨询', 17, 'add_userask');
INSERT INTO `auth_permission` VALUES (50, 'Can change 用户咨询', 17, 'change_userask');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 用户咨询', 17, 'delete_userask');
INSERT INTO `auth_permission` VALUES (52, 'Can add 课程评论', 18, 'add_coursecomment');
INSERT INTO `auth_permission` VALUES (53, 'Can change 课程评论', 18, 'change_coursecomment');
INSERT INTO `auth_permission` VALUES (54, 'Can delete 课程评论', 18, 'delete_coursecomment');
INSERT INTO `auth_permission` VALUES (55, 'Can add 用户收藏', 19, 'add_userfavorite');
INSERT INTO `auth_permission` VALUES (56, 'Can change 用户收藏', 19, 'change_userfavorite');
INSERT INTO `auth_permission` VALUES (57, 'Can delete 用户收藏', 19, 'delete_userfavorite');
INSERT INTO `auth_permission` VALUES (58, 'Can add 用户消息', 20, 'add_usermessage');
INSERT INTO `auth_permission` VALUES (59, 'Can change 用户消息', 20, 'change_usermessage');
INSERT INTO `auth_permission` VALUES (60, 'Can delete 用户消息', 20, 'delete_usermessage');
INSERT INTO `auth_permission` VALUES (61, 'Can add 用户课程', 21, 'add_usercourse');
INSERT INTO `auth_permission` VALUES (62, 'Can change 用户课程', 21, 'change_usercourse');
INSERT INTO `auth_permission` VALUES (63, 'Can delete 用户课程', 21, 'delete_usercourse');
INSERT INTO `auth_permission` VALUES (64, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (65, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (66, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (67, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (68, 'Can view 课程', 13, 'view_course');
INSERT INTO `auth_permission` VALUES (69, 'Can view 课程资源', 16, 'view_coursesource');
INSERT INTO `auth_permission` VALUES (70, 'Can view 章节', 14, 'view_lesson');
INSERT INTO `auth_permission` VALUES (71, 'Can view 视频', 15, 'view_video');
INSERT INTO `auth_permission` VALUES (72, 'Can view 课程评论', 18, 'view_coursecomment');
INSERT INTO `auth_permission` VALUES (73, 'Can view 用户咨询', 17, 'view_userask');
INSERT INTO `auth_permission` VALUES (74, 'Can view 用户课程', 21, 'view_usercourse');
INSERT INTO `auth_permission` VALUES (75, 'Can view 用户收藏', 19, 'view_userfavorite');
INSERT INTO `auth_permission` VALUES (76, 'Can view 用户消息', 20, 'view_usermessage');
INSERT INTO `auth_permission` VALUES (77, 'Can view 城市', 10, 'view_citydict');
INSERT INTO `auth_permission` VALUES (78, 'Can view 课程机构', 11, 'view_courseorg');
INSERT INTO `auth_permission` VALUES (79, 'Can view 教师', 12, 'view_teacher');
INSERT INTO `auth_permission` VALUES (80, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (81, 'Can view 轮播图', 9, 'view_banner');
INSERT INTO `auth_permission` VALUES (82, 'Can view 邮箱验证码', 8, 'view_emailverifyrecord');
INSERT INTO `auth_permission` VALUES (83, 'Can view 用户信息', 7, 'view_userprofile');
INSERT INTO `auth_permission` VALUES (84, 'Can add Bookmark', 22, 'add_bookmark');
INSERT INTO `auth_permission` VALUES (85, 'Can change Bookmark', 22, 'change_bookmark');
INSERT INTO `auth_permission` VALUES (86, 'Can delete Bookmark', 22, 'delete_bookmark');
INSERT INTO `auth_permission` VALUES (87, 'Can add User Setting', 23, 'add_usersettings');
INSERT INTO `auth_permission` VALUES (88, 'Can change User Setting', 23, 'change_usersettings');
INSERT INTO `auth_permission` VALUES (89, 'Can delete User Setting', 23, 'delete_usersettings');
INSERT INTO `auth_permission` VALUES (90, 'Can add User Widget', 24, 'add_userwidget');
INSERT INTO `auth_permission` VALUES (91, 'Can change User Widget', 24, 'change_userwidget');
INSERT INTO `auth_permission` VALUES (92, 'Can delete User Widget', 24, 'delete_userwidget');
INSERT INTO `auth_permission` VALUES (93, 'Can add log entry', 25, 'add_log');
INSERT INTO `auth_permission` VALUES (94, 'Can change log entry', 25, 'change_log');
INSERT INTO `auth_permission` VALUES (95, 'Can delete log entry', 25, 'delete_log');
INSERT INTO `auth_permission` VALUES (96, 'Can view Bookmark', 22, 'view_bookmark');
INSERT INTO `auth_permission` VALUES (97, 'Can view log entry', 25, 'view_log');
INSERT INTO `auth_permission` VALUES (98, 'Can view User Setting', 23, 'view_usersettings');
INSERT INTO `auth_permission` VALUES (99, 'Can view User Widget', 24, 'view_userwidget');
INSERT INTO `auth_permission` VALUES (100, 'Can add captcha store', 26, 'add_captchastore');
INSERT INTO `auth_permission` VALUES (101, 'Can change captcha store', 26, 'change_captchastore');
INSERT INTO `auth_permission` VALUES (102, 'Can delete captcha store', 26, 'delete_captchastore');
INSERT INTO `auth_permission` VALUES (103, 'Can view captcha store', 26, 'view_captchastore');
INSERT INTO `auth_permission` VALUES (104, 'Can view 轮播课程', 27, 'view_bannercourse');
INSERT INTO `auth_permission` VALUES (105, 'Can add 轮播课程', 13, 'add_bannercourse');
INSERT INTO `auth_permission` VALUES (106, 'Can change 轮播课程', 13, 'change_bannercourse');
INSERT INTO `auth_permission` VALUES (107, 'Can delete 轮播课程', 13, 'delete_bannercourse');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for captcha_captchastore
-- ----------------------------
DROP TABLE IF EXISTS `captcha_captchastore`;
CREATE TABLE `captcha_captchastore`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `response` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `hashkey` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expiration` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `hashkey`(`hashkey`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 99 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for courses_course
-- ----------------------------
DROP TABLE IF EXISTS `courses_course`;
CREATE TABLE `courses_course`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `detail` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `degree` varchar(5) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `learn_times` int(11) NOT NULL,
  `students` int(11) NOT NULL,
  `fav_nums` int(11) NOT NULL,
  `image` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `click_num` int(11) NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `course_org_id` int(11) DEFAULT NULL,
  `category` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tag` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `teacher_id` int(11) DEFAULT NULL,
  `teacher_tell` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `youneed_konw` varchar(300) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_banner` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `courses_course_11456c5a`(`course_org_id`) USING BTREE,
  INDEX `courses_course_d9614d40`(`teacher_id`) USING BTREE,
  CONSTRAINT `courses_cour_course_org_id_4d2c4aab_fk_organization_courseorg_id` FOREIGN KEY (`course_org_id`) REFERENCES `organization_courseorg` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `courses_course_teacher_id_846fa526_fk_organization_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `organization_teacher` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of courses_course
-- ----------------------------
INSERT INTO `courses_course` VALUES (1, 'django入门', 'django入门', 'Django入门', 'zj', 0, 0, 0, 'courses/2019/05/Koala.jpg', 4, '2019-05-08 15:00:00.000000', 1, '后端开发', 'python', NULL, '', '', 0);
INSERT INTO `courses_course` VALUES (2, '爬虫', '抓到好东西', '这是达内最牛逼的课程', 'zj', 1000, 10, 20, 'courses/2019/05/Desert.jpg', 12, '2019-05-16 20:16:00.000000', 2, '后端开发', 'python', NULL, '我们的都是好人', '这是一门没有用的课程', 0);
INSERT INTO `courses_course` VALUES (3, '嵌入式', '嵌入式的一个好课程', '这是达内的嵌入式的课程。', 'zj', 15, 100, 10, 'courses/2019/05/Penguins.jpg', 1018, '2019-05-16 20:17:00.000000', 3, '后端开发', 'IT', NULL, '', '', 0);
INSERT INTO `courses_course` VALUES (4, '七天学会python', '7天你学不会', '哈哈哈哈', 'zj', 50, 100, 20, 'courses/2019/05/Lighthouse.jpg', 21, '2019-05-16 20:17:00.000000', 4, '后端开发', 'python', NULL, '', '', 0);
INSERT INTO `courses_course` VALUES (5, '足球的自我修养', '我们都是好孩子', '哈哈哈哈', 'cj', 1, 2, 3, 'courses/2019/05/Koala_j0rWACd.jpg', 1019, '2019-05-16 20:18:00.000000', 5, '后端开发', 'IT', NULL, '你好呀。', '这是一门没有用的课程', 1);
INSERT INTO `courses_course` VALUES (6, '北京大学发展史', '我们都是北大的人', '我们都是一个好的学生', 'zj', 1, 3, 4, 'courses/2019/05/Koala_9ucNurQ.jpg', 240, '2019-05-16 20:19:00.000000', 6, '后端开发', '人文', NULL, '', '', 0);
INSERT INTO `courses_course` VALUES (7, 'numpy 的概述', '我们都是好孩子', '围绕富士达积分卡拉夫发货撒了个好看辣椒水就', 'gj', 23, 45, 23, 'courses/2019/05/Jellyfish.jpg', 104, '2019-05-16 20:19:00.000000', 7, '后端开发', '', NULL, '', '', 0);
INSERT INTO `courses_course` VALUES (8, '西安交大最牛逼的课程。', '一个创造奇迹的城市', '法法师方法士大夫沙发上任务二开了房哈斯脸红耳环会发生进口量大幅回UI温热后复活卡时间还多然后问饿哦我然后撒浩丰科技分散；了解 发对方立刻接娃儿、', 'gj', 23, 453, 23, 'courses/2019/05/Koala_gk4NT5b.jpg', 27, '2019-05-16 20:20:00.000000', 8, '后端开发', '', NULL, '', '', 0);
INSERT INTO `courses_course` VALUES (9, 'pandas', '这是数据分析的必修的课程', '发水电费计算机阿法拉设计费富士达积分离开家返利网科技福建省垃圾风口浪尖疼她阿发时代峻峰；了让我IE人陪去皮肉 、', 'gj', 2, 4, 234, 'courses/2019/05/Hydrangeas.jpg', 248, '2019-05-16 20:21:00.000000', 9, '后端开发', 'IT', NULL, '', '', 0);
INSERT INTO `courses_course` VALUES (10, '石油冶炼', '这是一个石油冶炼的活。', '我们都是一个好员工。', 'zj', 23, 46, 23, 'courses/2019/05/Lighthouse_tgcrUQS.jpg', 269, '2019-05-16 20:22:00.000000', 10, '后端开发', '石油', 1, '你来了就好好的学习，就完事了嗷。', '这是一个关于石油冶炼的课程，如果你没有关于石油方面的知识，那么你很难学的懂。', 0);
INSERT INTO `courses_course` VALUES (11, 'web前端课程', '这是一个牛逼的web 3.0', 'wopenfdsfkjasdhfhwauthffgadsfjkgvkjfnkjhuiwethytg8wreahgraewhgvajksdfvjavuiegfegfaeh;ashg;\r\nFHSJAHGUIAHGUIWWHG;KHV;KASH\r\nFHAJKGHFUIAHYT\r\ngadjg\'agioyhwqretakj;s\'gghajsgwy8\r\nghsjkahgiuhytiuhavnhjv;uihg', 'zj', 100, 3, 0, 'courses/2019/06/Chrysanthemum.jpg', 1, '2019-06-02 11:17:00.000000', 2, '后端开发', 'IT', 6, '哈哈哈', '多写多思考', 1);
INSERT INTO `courses_course` VALUES (12, '中国足球冲进了世界杯', '中国足球是个好东西', '<p style=\"line-height: 16px;\"><img style=\"vertical-align: middle; margin-right: 2px;\" src=\"http://127.0.0.1:8000/static/ueditor/dialogs/attachment/fileTypeImages/icon_txt.gif\"/><a style=\"font-size:12px; color:#0066cc;\" href=\"/media/course/resouce/2019/06/深圳民治中心-AID产品线-日报-2019-5-23-龚研.xlsx\" title=\"深圳民治中心-AID产品线-日报-2019-5-23-龚研.xlsx\">深圳民治中心-AID产品线-日报-2019-5-23-龚研.xlsx</a></p><p style=\"line-height: 16px;\"><strong>我们都是好孩子</strong><br/></p><p style=\"line-height: 16px;\"><strong><span style=\"text-decoration: underline;\">嗨嗨</span></strong></p><h1 label=\"标题居中\" style=\"font-size: 32px; font-weight: bold; border-bottom: 2px solid rgb(204, 204, 204); padding: 0px 4px 0px 0px; text-align: center; margin: 0px 0px 20px;\"><strong><span style=\"text-decoration: underline;\">你是个王爷爷<br/></span></strong></h1><p><img src=\"/course/ueditor/word_20190610231825_929.png\" title=\"\" alt=\"word.png\"/></p>', 'zj', 1000, 10, 0, 'courses/2019/06/word.png', 2, '2019-06-10 23:16:00.000000', 5, '后端开发', '人文', 2, '你要好好学', '这是一门没有用的课程', 0);

-- ----------------------------
-- Table structure for courses_coursesource
-- ----------------------------
DROP TABLE IF EXISTS `courses_coursesource`;
CREATE TABLE `courses_coursesource`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `download` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `courses_coursesource_course_id_436a963a_fk_courses_course_id`(`course_id`) USING BTREE,
  CONSTRAINT `courses_coursesource_course_id_436a963a_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of courses_coursesource
-- ----------------------------
INSERT INTO `courses_coursesource` VALUES (1, '如何提炼石油', 'course/resouce/2019/05/第8章_总结.rar', '2019-05-25 12:54:00.000000', 10);
INSERT INTO `courses_coursesource` VALUES (2, '如何磨洋工', 'course/resouce/2019/05/text.py', '2019-05-25 17:35:00.000000', 10);
INSERT INTO `courses_coursesource` VALUES (3, '我们的时代的资源', 'course/resouce/2019/06/深圳民治中心-AID产品线-日报-2019-5-23-龚研.xlsx', '2019-06-02 11:17:00.000000', 11);
INSERT INTO `courses_coursesource` VALUES (4, '我们的时代的资源', 'course/resouce/2019/06/word.png', '2019-06-10 23:16:00.000000', 12);

-- ----------------------------
-- Table structure for courses_lesson
-- ----------------------------
DROP TABLE IF EXISTS `courses_lesson`;
CREATE TABLE `courses_lesson`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `course_id` int(11) NOT NULL,
  `learn_times` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `courses_lesson_course_id_16bc4882_fk_courses_course_id`(`course_id`) USING BTREE,
  CONSTRAINT `courses_lesson_course_id_16bc4882_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of courses_lesson
-- ----------------------------
INSERT INTO `courses_lesson` VALUES (1, '中国足球', '2019-05-18 16:00:00.000000', 5, 10);
INSERT INTO `courses_lesson` VALUES (2, '国际足球', '2019-05-18 16:00:00.000000', 5, 20);
INSERT INTO `courses_lesson` VALUES (3, '辣鸡足球', '2019-05-18 16:01:00.000000', 5, 30);
INSERT INTO `courses_lesson` VALUES (4, '第一章 石油简述', '2019-05-25 12:37:00.000000', 10, 0);
INSERT INTO `courses_lesson` VALUES (5, '第二章 石油冶炼', '2019-05-25 12:37:00.000000', 10, 0);
INSERT INTO `courses_lesson` VALUES (6, '第三章 石油提取', '2019-05-25 12:38:00.000000', 10, 0);
INSERT INTO `courses_lesson` VALUES (7, '1.1 我们的时代', '2019-06-02 11:17:00.000000', 11, 23);
INSERT INTO `courses_lesson` VALUES (8, '1.1我们正处于一个好的时代', '2019-06-10 23:16:00.000000', 12, 12);
INSERT INTO `courses_lesson` VALUES (9, '2.1 我们都是好孩子', '2019-06-10 23:16:00.000000', 12, 124);

-- ----------------------------
-- Table structure for courses_video
-- ----------------------------
DROP TABLE IF EXISTS `courses_video`;
CREATE TABLE `courses_video`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `lesson_id` int(11) NOT NULL,
  `url` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `learn_times` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `courses_video_lesson_id_59f2396e_fk_courses_lesson_id`(`lesson_id`) USING BTREE,
  CONSTRAINT `courses_video_lesson_id_59f2396e_fk_courses_lesson_id` FOREIGN KEY (`lesson_id`) REFERENCES `courses_lesson` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of courses_video
-- ----------------------------
INSERT INTO `courses_video` VALUES (1, '搞笑的中国足球', '2019-05-18 16:05:00.000000', 1, 'http:www.biibili.com/p/41231253', 0);
INSERT INTO `courses_video` VALUES (2, '这是一个外部跳转的视频', '2019-05-18 16:09:00.000000', 2, 'http:www.biibili.com/p/412', 0);
INSERT INTO `courses_video` VALUES (3, '垃圾足球', '2019-05-18 16:09:00.000000', 3, 'http:www.biibili.com/p/4123342432', 0);
INSERT INTO `courses_video` VALUES (4, '我们的时代', '2019-05-25 12:38:00.000000', 6, '3.1 伟大的胜利油田', 0);
INSERT INTO `courses_video` VALUES (5, '2.1 石油的好处', '2019-05-25 12:39:00.000000', 5, 'www.baidu.com', 0);

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (26, 'captcha', 'captchastore');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (27, 'courses', 'bannercourse');
INSERT INTO `django_content_type` VALUES (13, 'courses', 'course');
INSERT INTO `django_content_type` VALUES (16, 'courses', 'coursesource');
INSERT INTO `django_content_type` VALUES (14, 'courses', 'lesson');
INSERT INTO `django_content_type` VALUES (15, 'courses', 'video');
INSERT INTO `django_content_type` VALUES (18, 'operations', 'coursecomment');
INSERT INTO `django_content_type` VALUES (17, 'operations', 'userask');
INSERT INTO `django_content_type` VALUES (21, 'operations', 'usercourse');
INSERT INTO `django_content_type` VALUES (19, 'operations', 'userfavorite');
INSERT INTO `django_content_type` VALUES (20, 'operations', 'usermessage');
INSERT INTO `django_content_type` VALUES (10, 'organization', 'citydict');
INSERT INTO `django_content_type` VALUES (11, 'organization', 'courseorg');
INSERT INTO `django_content_type` VALUES (12, 'organization', 'teacher');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (9, 'users', 'banner');
INSERT INTO `django_content_type` VALUES (8, 'users', 'emailverifyrecord');
INSERT INTO `django_content_type` VALUES (7, 'users', 'userprofile');
INSERT INTO `django_content_type` VALUES (22, 'xadmin', 'bookmark');
INSERT INTO `django_content_type` VALUES (25, 'xadmin', 'log');
INSERT INTO `django_content_type` VALUES (23, 'xadmin', 'usersettings');
INSERT INTO `django_content_type` VALUES (24, 'xadmin', 'userwidget');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 51 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2019-04-03 07:40:00.909624');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2019-04-03 07:40:01.575662');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2019-04-03 07:40:01.778674');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2019-04-03 07:40:01.806675');
INSERT INTO `django_migrations` VALUES (5, 'contenttypes', '0002_remove_content_type_name', '2019-04-03 07:40:01.919682');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0002_alter_permission_name_max_length', '2019-04-03 07:40:01.987685');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0003_alter_user_email_max_length', '2019-04-03 07:40:02.135694');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0004_alter_user_username_opts', '2019-04-03 07:40:02.252701');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0005_alter_user_last_login_null', '2019-04-03 07:40:02.614721');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0006_require_contenttypes_0002', '2019-04-03 07:40:02.627722');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0007_alter_validators_add_error_messages', '2019-04-03 07:40:02.638723');
INSERT INTO `django_migrations` VALUES (12, 'sessions', '0001_initial', '2019-04-03 07:40:02.809732');
INSERT INTO `django_migrations` VALUES (13, 'users', '0001_initial', '2019-04-03 07:56:23.449822');
INSERT INTO `django_migrations` VALUES (14, 'courses', '0001_initial', '2019-04-03 09:33:43.193836');
INSERT INTO `django_migrations` VALUES (15, 'operations', '0001_initial', '2019-04-03 09:33:44.266898');
INSERT INTO `django_migrations` VALUES (16, 'organization', '0001_initial', '2019-04-03 09:33:45.368961');
INSERT INTO `django_migrations` VALUES (17, 'users', '0002_banner_emailverifyrecord', '2019-04-03 09:33:45.619975');
INSERT INTO `django_migrations` VALUES (18, 'xadmin', '0001_initial', '2019-04-04 10:28:23.503939');
INSERT INTO `django_migrations` VALUES (19, 'xadmin', '0002_log', '2019-04-04 10:28:23.839958');
INSERT INTO `django_migrations` VALUES (20, 'xadmin', '0003_auto_20160715_0100', '2019-04-04 10:28:23.932964');
INSERT INTO `django_migrations` VALUES (21, 'users', '0003_auto_20190404_1041', '2019-04-04 10:41:12.232908');
INSERT INTO `django_migrations` VALUES (22, 'users', '0004_auto_20190404_1042', '2019-04-04 10:42:43.777144');
INSERT INTO `django_migrations` VALUES (23, 'captcha', '0001_initial', '2019-05-06 18:29:15.726842');
INSERT INTO `django_migrations` VALUES (24, 'organization', '0002_courseorg_category', '2019-05-07 17:51:39.391623');
INSERT INTO `django_migrations` VALUES (25, 'organization', '0003_auto_20190507_1752', '2019-05-07 17:52:44.166328');
INSERT INTO `django_migrations` VALUES (26, 'organization', '0004_auto_20190508_1020', '2019-05-08 10:20:24.358051');
INSERT INTO `django_migrations` VALUES (27, 'organization', '0002_teacher_desc', '2019-05-08 14:25:11.652866');
INSERT INTO `django_migrations` VALUES (28, 'organization', '0003_auto_20190508_1437', '2019-05-08 14:37:33.364289');
INSERT INTO `django_migrations` VALUES (29, 'courses', '0002_course_course_org', '2019-05-08 14:37:33.670307');
INSERT INTO `django_migrations` VALUES (30, 'courses', '0003_auto_20190508_1449', '2019-05-08 14:49:21.933817');
INSERT INTO `django_migrations` VALUES (31, 'courses', '0004_auto_20190508_1527', '2019-05-08 15:27:43.909482');
INSERT INTO `django_migrations` VALUES (32, 'courses', '0005_remove_course_course_org', '2019-05-08 15:43:53.636948');
INSERT INTO `django_migrations` VALUES (33, 'organization', '0005_merge', '2019-05-08 17:25:50.805830');
INSERT INTO `django_migrations` VALUES (34, 'courses', '0006_course_course_org', '2019-05-08 17:25:51.159850');
INSERT INTO `django_migrations` VALUES (35, 'organization', '0006_teacher_image', '2019-05-08 17:34:40.652135');
INSERT INTO `django_migrations` VALUES (36, 'organization', '0007_auto_20190508_1734', '2019-05-08 17:34:40.740140');
INSERT INTO `django_migrations` VALUES (37, 'courses', '0007_course_category', '2019-05-17 17:03:14.921598');
INSERT INTO `django_migrations` VALUES (38, 'courses', '0008_course_tag', '2019-05-17 17:56:32.456487');
INSERT INTO `django_migrations` VALUES (39, 'courses', '0009_auto_20190518_1608', '2019-05-18 16:08:15.642859');
INSERT INTO `django_migrations` VALUES (40, 'courses', '0010_video_learn_times', '2019-05-25 12:51:04.537595');
INSERT INTO `django_migrations` VALUES (41, 'courses', '0011_course_teacher', '2019-05-25 13:05:38.075559');
INSERT INTO `django_migrations` VALUES (42, 'courses', '0012_auto_20190525_1332', '2019-05-25 13:33:01.645565');
INSERT INTO `django_migrations` VALUES (43, 'organization', '0008_teacher_age', '2019-05-27 23:51:04.332564');
INSERT INTO `django_migrations` VALUES (44, 'organization', '0009_auto_20190527_2352', '2019-05-27 23:52:28.061353');
INSERT INTO `django_migrations` VALUES (45, 'users', '0005_auto_20190530_0016', '2019-05-30 00:16:53.359425');
INSERT INTO `django_migrations` VALUES (46, 'users', '0006_auto_20190530_2101', '2019-05-30 21:01:56.638045');
INSERT INTO `django_migrations` VALUES (47, 'courses', '0013_course_is_banner', '2019-06-01 00:20:21.505439');
INSERT INTO `django_migrations` VALUES (48, 'users', '0007_auto_20190601_0031', '2019-06-01 00:32:10.595996');
INSERT INTO `django_migrations` VALUES (49, 'organization', '0010_courseorg_tag', '2019-06-01 01:09:54.442481');
INSERT INTO `django_migrations` VALUES (50, 'courses', '0014_auto_20190610_2246', '2019-06-10 22:46:50.803759');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_de54fa62`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('10djf01cszu0eab029ujpl0qcw4po7dg', 'ZTBiYTA4NjA0MGI2NzlkODgzNWFkMjc2MDI5YTAxZjVkYzg4ZmJhYjp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijc0OTgxNTE1MjBiNGMxOWQxNmFiNzRkMzAzMzkzYjFmNjg2ZWQxNzciLCJMSVNUX1FVRVJZIjpbWyJvcmdhbml6YXRpb24iLCJ0ZWFjaGVyIl0sIiJdfQ==', '2019-05-22 21:16:56.309891');
INSERT INTO `django_session` VALUES ('6ucsugdxni8v4nm4ue6gpa9fpmq8gcuj', 'MTUzYjQzNTg3NWRhMTQ2MGNmOWViMWM4Y2IzNWIzYmJkNGFlZjQwYTp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjcyNjkyNDM4OTUzYzkxYWRkN2VkNjJlNDFlMjRlNDdhNDY0NDc4NzkifQ==', '2019-06-26 17:21:02.828991');
INSERT INTO `django_session` VALUES ('ia2d08iha0j8nyssq2ifbua9ub2sxtdm', 'ODBlZDNhNDMwOTllZDY5ODcwYzYyYjE3NDY4YWNkNjM4MzYxYWRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjIzMTllNGY1YjIzY2U0NGY4OTQ2ZjkyZTVkOGQwZTM0NjY0ODUzZjcifQ==', '2019-05-20 17:30:09.093986');
INSERT INTO `django_session` VALUES ('lljc3p0yo2grrkcxkcngcbkliv0benrg', 'ODBlZDNhNDMwOTllZDY5ODcwYzYyYjE3NDY4YWNkNjM4MzYxYWRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjIzMTllNGY1YjIzY2U0NGY4OTQ2ZjkyZTVkOGQwZTM0NjY0ODUzZjcifQ==', '2019-05-20 15:54:59.573420');
INSERT INTO `django_session` VALUES ('twu0x90bp3o07nys8rfdpwh3wxq5ln0m', 'YWViMjc3M2QzMjIxZjlmMTFiNGJkMTJjOWExYzBiZGUzZWE5NWJhMzp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjcyNjkyNDM4OTUzYzkxYWRkN2VkNjJlNDFlMjRlNDdhNDY0NDc4NzkiLCJMSVNUX1FVRVJZIjpbWyJjb3Vyc2VzIiwiY291cnNlIl0sIiJdfQ==', '2019-06-16 13:51:02.466341');
INSERT INTO `django_session` VALUES ('ulp1aqvlbasbdz164609coe8jf8zhlrz', 'ZDNlNzQzOTE1ZTE3YTkzYWUzZTY4MzljOGJkMWEzNzQ2MTU3OTY4ODp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijc0OTgxNTE1MjBiNGMxOWQxNmFiNzRkMzAzMzkzYjFmNjg2ZWQxNzciLCJMSVNUX1FVRVJZIjpbWyJjb3Vyc2VzIiwidmlkZW8iXSwiIl19', '2019-06-01 16:08:58.921334');
INSERT INTO `django_session` VALUES ('urziz8rxqz5y2k9dhanr8rlyhhkze2vr', 'NDIwZDg4ZjdhNzk4MzE0YzlkNDBiZjI5YWZiNDg1ZGM2NWFiMDdhMzp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjAyMTAzZDQzODJhMGQ2ZDE1MDJlZGY2OTM0YjcwOTg1MzE0Y2RhMjgifQ==', '2019-05-21 16:12:43.505110');
INSERT INTO `django_session` VALUES ('vnvkqch87f8p71oz3fulet0deiborjx9', 'MTA2ODA1NTIxOTViNTNiMTA2NDcwZDFkYzYxNDc4NTViZWRkOWMxNjp7Il9hdXRoX3VzZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6Ijc0OTgxNTE1MjBiNGMxOWQxNmFiNzRkMzAzMzkzYjFmNjg2ZWQxNzcifQ==', '2019-05-30 17:59:01.563266');
INSERT INTO `django_session` VALUES ('wdok5bauwb2ovax7ca3apgmn3b4jhd4s', 'ODZjNmI1ZmY0NjQ3MjViYTUzNDY2MTRkMzY4Y2I3ZjlmMjJiMzE1NDp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjBjZjY0ZjRjYmZiODMwOGE5ZDk2MzFjMzgyZDAyZmQ5MjU1MjJmYzYifQ==', '2019-05-20 20:26:14.501293');
INSERT INTO `django_session` VALUES ('xkwns77n9fweyvl8ko0co15dj85zgnla', 'ODBlZDNhNDMwOTllZDY5ODcwYzYyYjE3NDY4YWNkNjM4MzYxYWRiNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoidXNlcnMudmlld3MuQ3VzdG9tQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjIzMTllNGY1YjIzY2U0NGY4OTQ2ZjkyZTVkOGQwZTM0NjY0ODUzZjcifQ==', '2019-05-20 15:18:21.017670');
INSERT INTO `django_session` VALUES ('z4sz0jaxlu5d9plchdqvxcjemf4b7r2j', 'ZTZlYmVmZmFiOTgwYTNhYzI3OTFmM2E1ODMzZWVlNWMzYzU0YjkyNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzE5ZTRmNWIyM2NlNDRmODk0NmY5MmU1ZDhkMGUzNDY2NDg1M2Y3IiwiTElTVF9RVUVSWSI6W1sieGFkbWluIiwibG9nIl0sIiJdfQ==', '2019-04-29 10:02:52.114589');

-- ----------------------------
-- Table structure for operations_coursecomment
-- ----------------------------
DROP TABLE IF EXISTS `operations_coursecomment`;
CREATE TABLE `operations_coursecomment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comments` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `course_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `operations_coursecomment_course_id_ee3f9947_fk_courses_course_id`(`course_id`) USING BTREE,
  INDEX `operations_coursecommen_user_id_6e14aa25_fk_users_userprofile_id`(`user_id`) USING BTREE,
  CONSTRAINT `operations_coursecommen_user_id_6e14aa25_fk_users_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `operations_coursecomment_course_id_ee3f9947_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operations_coursecomment
-- ----------------------------
INSERT INTO `operations_coursecomment` VALUES (1, '', '2019-05-25 18:40:41.746281', 10, 5);
INSERT INTO `operations_coursecomment` VALUES (2, '你好', '2019-05-25 18:42:05.774088', 10, 5);
INSERT INTO `operations_coursecomment` VALUES (3, '你好吗', '2019-05-25 18:42:16.604707', 10, 5);
INSERT INTO `operations_coursecomment` VALUES (4, '你好', '2019-05-25 18:46:21.464712', 10, 5);
INSERT INTO `operations_coursecomment` VALUES (5, '你好吗', '2019-05-25 18:54:50.786844', 10, 5);
INSERT INTO `operations_coursecomment` VALUES (6, '你好吗', '2019-05-25 18:54:51.986912', 10, 5);
INSERT INTO `operations_coursecomment` VALUES (7, '你好吗', '2019-05-25 18:54:59.625349', 10, 5);
INSERT INTO `operations_coursecomment` VALUES (8, '你好吗', '2019-05-25 18:55:01.112434', 10, 5);

-- ----------------------------
-- Table structure for operations_userask
-- ----------------------------
DROP TABLE IF EXISTS `operations_userask`;
CREATE TABLE `operations_userask`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `course_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operations_userask
-- ----------------------------
INSERT INTO `operations_userask` VALUES (1, '特朗普', '12346579810', 'nick', '2019-05-08 11:42:49.319887');
INSERT INTO `operations_userask` VALUES (2, '小王', '11111111111', 'fas', '2019-05-08 11:43:51.535445');
INSERT INTO `operations_userask` VALUES (3, 'xiaowang', '18667018590', 'django', '2019-05-08 11:53:08.083278');

-- ----------------------------
-- Table structure for operations_usercourse
-- ----------------------------
DROP TABLE IF EXISTS `operations_usercourse`;
CREATE TABLE `operations_usercourse`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `add_time` datetime(6) NOT NULL,
  `course_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `operations_usercourse_course_id_a9f30cc6_fk_courses_course_id`(`course_id`) USING BTREE,
  INDEX `operations_usercourse_user_id_d33454be_fk_users_userprofile_id`(`user_id`) USING BTREE,
  CONSTRAINT `operations_usercourse_course_id_a9f30cc6_fk_courses_course_id` FOREIGN KEY (`course_id`) REFERENCES `courses_course` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `operations_usercourse_user_id_d33454be_fk_users_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operations_usercourse
-- ----------------------------
INSERT INTO `operations_usercourse` VALUES (1, '2019-05-17 17:10:00.000000', 5, 5);
INSERT INTO `operations_usercourse` VALUES (2, '2019-05-17 17:11:00.000000', 5, 1);
INSERT INTO `operations_usercourse` VALUES (3, '2019-05-17 17:11:00.000000', 5, 2);
INSERT INTO `operations_usercourse` VALUES (4, '2019-05-25 22:38:16.914173', 9, 5);
INSERT INTO `operations_usercourse` VALUES (5, '2019-05-25 22:38:34.400174', 8, 5);
INSERT INTO `operations_usercourse` VALUES (6, '2019-05-25 22:41:25.502960', 7, 5);
INSERT INTO `operations_usercourse` VALUES (7, '2019-05-28 18:37:04.727381', 10, 5);
INSERT INTO `operations_usercourse` VALUES (8, '2019-06-11 19:13:32.810093', 11, 5);

-- ----------------------------
-- Table structure for operations_userfavorite
-- ----------------------------
DROP TABLE IF EXISTS `operations_userfavorite`;
CREATE TABLE `operations_userfavorite`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fav_id` int(11) NOT NULL,
  `fav_type` int(11) NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `operations_userfavorite_user_id_092d3821_fk_users_userprofile_id`(`user_id`) USING BTREE,
  CONSTRAINT `operations_userfavorite_user_id_092d3821_fk_users_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operations_userfavorite
-- ----------------------------
INSERT INTO `operations_userfavorite` VALUES (7, 1, 3, '2019-05-28 22:17:12.388990', 5);
INSERT INTO `operations_userfavorite` VALUES (12, 10, 1, '2019-05-31 00:29:02.943799', 5);

-- ----------------------------
-- Table structure for operations_usermessage
-- ----------------------------
DROP TABLE IF EXISTS `operations_usermessage`;
CREATE TABLE `operations_usermessage`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `message` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `has_read` tinyint(1) NOT NULL,
  `add_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of operations_usermessage
-- ----------------------------
INSERT INTO `operations_usermessage` VALUES (1, 5, '欢饮注册达内教育', 1, '2019-05-31 22:35:00.000000');

-- ----------------------------
-- Table structure for organization_citydict
-- ----------------------------
DROP TABLE IF EXISTS `organization_citydict`;
CREATE TABLE `organization_citydict`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of organization_citydict
-- ----------------------------
INSERT INTO `organization_citydict` VALUES (1, '北京市', '我们的首都', '2019-05-07 17:13:00.000000');
INSERT INTO `organization_citydict` VALUES (2, '上海市', '一个有活力的城市', '2019-05-07 17:13:00.000000');
INSERT INTO `organization_citydict` VALUES (3, '深圳市', '一个创造奇迹的城市', '2019-05-07 17:14:00.000000');
INSERT INTO `organization_citydict` VALUES (4, '西安市', '一个古老的城市', '2019-05-07 17:14:00.000000');
INSERT INTO `organization_citydict` VALUES (5, '蔡家坡', '中国的蔡家坡，世界的新加坡', '2019-05-07 17:15:00.000000');

-- ----------------------------
-- Table structure for organization_courseorg
-- ----------------------------
DROP TABLE IF EXISTS `organization_courseorg`;
CREATE TABLE `organization_courseorg`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `desc` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `click_nums` int(11) NOT NULL,
  `fav_nums` int(11) NOT NULL,
  `image` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `address` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_time` datetime(6) NOT NULL,
  `city_id` int(11) NOT NULL,
  `category` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `course_num` int(11) NOT NULL,
  `students` int(11) NOT NULL,
  `tag` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `organization_course_city_id_4a842f85_fk_organization_citydict_id`(`city_id`) USING BTREE,
  CONSTRAINT `organization_course_city_id_4a842f85_fk_organization_citydict_id` FOREIGN KEY (`city_id`) REFERENCES `organization_citydict` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of organization_courseorg
-- ----------------------------
INSERT INTO `organization_courseorg` VALUES (1, '传智播客', '传智播客是致力于高素质软件开发人才培养的新三板挂牌公司（代码：839976）。旗下已涵盖黑马程序员及博学谷两大子品牌。现开设JavaEE、Android、PHP、UI、IOS、前端、C++、网络营销、Python、云计算、全栈工程师、产品经理等培训学科，直营分校遍布北京、上海、广州、深圳、武汉、郑州、西安、哈尔滨、长沙、济南、重庆、南京、杭州、成都、石家庄、合肥等。', 12, 0, 'org/2019/05/logo.png', '北京市', '2019-05-07 17:16:00.000000', 1, 'pxjg', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (2, '达内教育', '达内专注职业教育16年，高薪聘请名师授课 ，采用“先学习，就业后付款”模式，帮助60万名学员成功就业。22大热门课程，60个城市,200家培训中心,一地学习,全国就业.要培训,就选上市公司!', 1, 0, 'org/2019/05/u5735893043448813930fm26gp0.jpg', '北京市', '2019-05-07 17:21:00.000000', 1, 'pxjg', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (3, '千峰教育', '千锋教育隶属于北京千锋互联科技有限公司，一直秉承“用良心做教育”的理念，公司总部位于北京，‘免费试学两周，满意后再报名’体验教学水平，免费提供学习视频下载。', 40, 0, 'org/2019/05/qf.jpg', '北京市', '2019-05-07 17:22:00.000000', 1, 'pxjg', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (4, '爱数圈', '这几年大数据的火热也带动了数据产业的爆发式的增长，但每一个风口都有自己的生命周期，火热之后就是理性的前进，那么大数据也是一样就目前来讲除了程序员，数据分析对于大众来讲还是很容', 0, 0, 'org/2019/05/80x60.png', '广州是增城区', '2019-05-07 17:24:00.000000', 2, 'gr', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (5, '懂球帝', '“懂球帝”，体育界网络热词，指的是极其精通对球类运动（尤其是足球和篮球）的知识的人，该词语是中性词汇，可以用来夸赞对球类运动十分在行的人，也可以用来讽刺那些对球类运动不懂装懂的人。', 25, 0, 'org/2019/05/dqd.jpg', '陕西省宝鸡市', '2019-05-07 17:26:00.000000', 5, 'gx', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (6, '北京大学', '一个优点牛逼的学校、。', 8, 0, 'org/2019/05/bd.jpg', '上海市浦东新区', '2019-05-07 17:27:00.000000', 2, 'gx', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (7, '清华大学', '比北大还厉害一点点的学校。', 0, 0, 'org/2019/05/qh.jpg', '深圳市大湾区', '2019-05-07 17:28:00.000000', 3, 'gr', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (8, '西安交通大学', '在西北地区排的上号的一个大学。', 81, 0, 'org/2019/05/xa.jpg', '西安市双府新家园', '2019-05-07 17:29:00.000000', 4, 'pxjg', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (9, '斯坦福大学', '国外一个有点著名的大学。', 2, 0, 'org/2019/05/stf.jpg', '美国伊利诺伊', '2019-05-07 17:31:00.000000', 4, 'gr', 0, 0, '全国知名');
INSERT INTO `organization_courseorg` VALUES (10, '北京石油化工学院', '我的一个同学在这儿上学而已！', 1, 0, 'org/2019/05/bjsh.jpg', '北京市大兴区', '2019-05-07 17:33:00.000000', 1, 'gx', 0, 0, '全国知名');

-- ----------------------------
-- Table structure for organization_teacher
-- ----------------------------
DROP TABLE IF EXISTS `organization_teacher`;
CREATE TABLE `organization_teacher`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `work_years` int(11) NOT NULL,
  `work_company` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `work_position` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `points` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `click_nums` int(11) NOT NULL,
  `fav_nums` int(11) NOT NULL,
  `org_id` int(11) NOT NULL,
  `desc` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `image` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `age` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `organization_teache_org_id_cd000a1a_fk_organization_courseorg_id`(`org_id`) USING BTREE,
  CONSTRAINT `organization_teache_org_id_cd000a1a_fk_organization_courseorg_id` FOREIGN KEY (`org_id`) REFERENCES `organization_courseorg` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of organization_teacher
-- ----------------------------
INSERT INTO `organization_teacher` VALUES (1, '史塔克', 5, '临冬城', '城主', '严厉', 6, 10, 1, '一个很严厉的长者！', 'teacher/2019/05/Desert.jpg', 0);
INSERT INTO `organization_teacher` VALUES (2, '詹姆', 2, '兰尼斯特', '太子', '浪荡', 122, 2, 2, '一个浪人', 'teacher/2019/05/Lighthouse.jpg', 0);
INSERT INTO `organization_teacher` VALUES (3, '夜王', 8, '异鬼公司', 'boss', '可以召唤很多异鬼', 20, 15, 3, '一个老的异鬼。', 'teacher/2019/05/Jellyfish.jpg', 0);
INSERT INTO `organization_teacher` VALUES (4, '小马哥', 5, '甲骨文', '程序员', '认真负责', 4, 2, 4, '一个老师', 'teacher/2019/05/Hydrangeas.jpg', 0);
INSERT INTO `organization_teacher` VALUES (5, '团团', 5, '多格科技', '董事长', '15', 3, 3, 5, '一个老师', 'teacher/2019/05/Tulips.jpg', 0);
INSERT INTO `organization_teacher` VALUES (6, '施一公', 20, '西湖大学', '校长', '有很多技能', 4, 4, 6, '一个老师', 'teacher/2019/05/Penguins.jpg', 0);
INSERT INTO `organization_teacher` VALUES (7, '王琪', 1, '广西大学', '学生', '认真负责', 5, 2, 7, '一个老师', 'teacher/2019/05/Koala.jpg', 0);
INSERT INTO `organization_teacher` VALUES (8, '牛犇', 10, '巨硬', 'cfo', '吹牛', 10, 20, 1, '一个老师', 'teacher/2019/05/Tulips_1n56k3X.jpg', 0);

-- ----------------------------
-- Table structure for users_banner
-- ----------------------------
DROP TABLE IF EXISTS `users_banner`;
CREATE TABLE `users_banner`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `image` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `url` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `index` int(11) NOT NULL,
  `add_time` date NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_banner
-- ----------------------------
INSERT INTO `users_banner` VALUES (1, '来了就是深圳人。', 'banner/2019/06/Desert.jpg', 'https://www.baidu.com', 1, '2019-06-01');
INSERT INTO `users_banner` VALUES (2, '深圳赚钱深圳花', 'banner/2019/06/Hydrangeas.jpg', 'https://www.baidu.com', 2, '2019-06-01');
INSERT INTO `users_banner` VALUES (3, '一分别想带回家', 'banner/2019/06/Tulips.jpg', 'https://www.baidu.com', 3, '2019-06-01');
INSERT INTO `users_banner` VALUES (4, '我们都说好人', 'banner/2019/06/Hydrangeas_LKOXX04.jpg', 'https://www.baidu.com', 4, '2019-06-01');
INSERT INTO `users_banner` VALUES (5, '你说你什么呢', 'banner/2019/06/Jellyfish.jpg', 'https://www.baidu.com', 5, '2019-06-01');

-- ----------------------------
-- Table structure for users_emailverifyrecord
-- ----------------------------
DROP TABLE IF EXISTS `users_emailverifyrecord`;
CREATE TABLE `users_emailverifyrecord`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `send_type` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `send_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_emailverifyrecord
-- ----------------------------
INSERT INTO `users_emailverifyrecord` VALUES (7, '12345', 'nihao@qq.com', 'register', '2019-04-04 11:06:00.000000');
INSERT INTO `users_emailverifyrecord` VALUES (8, 'admin', '123@qq.com', 'register', '2019-04-04 11:10:00.000000');
INSERT INTO `users_emailverifyrecord` VALUES (9, 'xmtd8F2YT1ZljI41', ' 842549758@qq.com', 'register', '2019-05-06 20:22:03.224921');
INSERT INTO `users_emailverifyrecord` VALUES (10, 'hOrnhRedLxT5J0C3', '292478354@qq.com', 'register', '2019-05-06 20:25:12.996775');
INSERT INTO `users_emailverifyrecord` VALUES (11, 'J3qFMVtmQuJFrYHK', 'franck_gxu@outlook.com', 'register', '2019-05-07 09:54:52.782419');
INSERT INTO `users_emailverifyrecord` VALUES (12, 'kTK47Y3gVH8RxvPG', '842549758@qq.com', 'forget', '2019-05-07 14:41:10.711940');
INSERT INTO `users_emailverifyrecord` VALUES (13, '3FZi', '249155836@qq.com', 'update_email', '2019-05-30 21:03:44.151195');
INSERT INTO `users_emailverifyrecord` VALUES (14, 'dc3O', '976464507@qq.com', 'update_email', '2019-05-30 21:29:49.188710');
INSERT INTO `users_emailverifyrecord` VALUES (15, '4937WRS5CqEImcGv', 'franck_gxu@outlook.com', 'forget', '2019-06-11 19:15:50.086945');
INSERT INTO `users_emailverifyrecord` VALUES (16, 'R5B17pVjhaqKMyIQ', '842549758@qq.com', 'forget', '2019-06-12 17:13:41.722761');
INSERT INTO `users_emailverifyrecord` VALUES (17, 'OK0u', 'maoxin176@163.com', 'update_email', '2019-06-12 17:27:01.383499');

-- ----------------------------
-- Table structure for users_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `users_userprofile`;
CREATE TABLE `users_userprofile`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `nick_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `birthday` date DEFAULT NULL,
  `gender` varchar(6) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `address` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `mobile` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `image` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_userprofile
-- ----------------------------
INSERT INTO `users_userprofile` VALUES (1, 'pbkdf2_sha256$24000$cf59FVv9n46X$ytOZ+GoYgOj2rVEd3liVLL/vqjFq2NWBPWj3TsQgzUg=', '2019-05-06 17:30:09.086986', 1, 'root', '', '', '', 1, 1, '2019-04-03 09:40:29.744089', '', NULL, 'female', '', NULL, 'courses/2019/05/Koala_j0rWACd.jpg');
INSERT INTO `users_userprofile` VALUES (2, 'pbkdf2_sha256$24000$DbtRSFYkS6ue$r6ipJci8JsDIm/lZVA/5K983jVX7fIRIDeP8WyDaTbM=', '2019-06-02 10:48:30.231216', 0, '842549758@qq.com', '', '', '842549758@qq.com', 1, 1, '2019-05-06 20:22:00.000000', 'xiaogang', '2019-06-12', 'female', '北京市', '18667018590', 'image/defaule.png');
INSERT INTO `users_userprofile` VALUES (3, 'pbkdf2_sha256$24000$LMIv2ECmTFWY$vQ+wOo17Gb/Jdae6xPMdo2ho3uISe7LA8o0AbZrU2Qs=', '2019-05-07 16:08:41.191250', 0, '292478354@qq.com', '', '', '292478354@qq.com', 0, 1, '2019-05-06 20:25:12.945772', '', NULL, 'female', '', NULL, 'image/defaule.png');
INSERT INTO `users_userprofile` VALUES (4, 'pbkdf2_sha256$24000$dm3gVmDA9S1m$sbTLkOTBqnzUXYwtssIywy6EA01bJOyAeLUvwuj2btY=', NULL, 0, 'franck_gxu@outlook.com', '', '', 'franck_gxu@outlook.com', 0, 1, '2019-05-07 09:54:52.727415', '', NULL, 'female', '', NULL, 'image/defaule.png');
INSERT INTO `users_userprofile` VALUES (5, 'pbkdf2_sha256$24000$PRnQky3ucRdz$4w38CiGG9K1oeK1nABz/9XycRIL4Dq0mfrzTbrWAL1g=', '2019-06-12 17:21:02.818991', 1, 'root1', '', '', 'maoxin176@163.com', 1, 1, '2019-05-07 17:12:07.790975', '小王', '2019-05-07', 'female', '我来之火星', '', 'image/2019/05/Jellyfish.jpg');

-- ----------------------------
-- Table structure for users_userprofile_groups
-- ----------------------------
DROP TABLE IF EXISTS `users_userprofile_groups`;
CREATE TABLE `users_userprofile_groups`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `users_userprofile_groups_userprofile_id_823cf2fc_uniq`(`userprofile_id`, `group_id`) USING BTREE,
  INDEX `users_userprofile_groups_group_id_3de53dbf_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `users_userprofil_userprofile_id_a4496a80_fk_users_userprofile_id` FOREIGN KEY (`userprofile_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `users_userprofile_groups_group_id_3de53dbf_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_userprofile_groups
-- ----------------------------
INSERT INTO `users_userprofile_groups` VALUES (1, 2, 1);

-- ----------------------------
-- Table structure for users_userprofile_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `users_userprofile_user_permissions`;
CREATE TABLE `users_userprofile_user_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `users_userprofile_user_permissions_userprofile_id_d0215190_uniq`(`userprofile_id`, `permission_id`) USING BTREE,
  INDEX `users_userprofile_u_permission_id_393136b6_fk_auth_permission_id`(`permission_id`) USING BTREE,
  CONSTRAINT `users_userprofil_userprofile_id_34544737_fk_users_userprofile_id` FOREIGN KEY (`userprofile_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `users_userprofile_u_permission_id_393136b6_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users_userprofile_user_permissions
-- ----------------------------
INSERT INTO `users_userprofile_user_permissions` VALUES (1, 2, 82);

-- ----------------------------
-- Table structure for xadmin_bookmark
-- ----------------------------
DROP TABLE IF EXISTS `xadmin_bookmark`;
CREATE TABLE `xadmin_bookmark`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `url_name` varchar(64) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `query` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_share` tinyint(1) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `xadmin_bookma_content_type_id_60941679_fk_django_content_type_id`(`content_type_id`) USING BTREE,
  INDEX `xadmin_bookmark_user_id_42d307fc_fk_users_userprofile_id`(`user_id`) USING BTREE,
  CONSTRAINT `xadmin_bookma_content_type_id_60941679_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `xadmin_bookmark_user_id_42d307fc_fk_users_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for xadmin_log
-- ----------------------------
DROP TABLE IF EXISTS `xadmin_log`;
CREATE TABLE `xadmin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `ip_addr` char(39) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id`(`content_type_id`) USING BTREE,
  INDEX `xadmin_log_user_id_bb16a176_fk_users_userprofile_id`(`user_id`) USING BTREE,
  CONSTRAINT `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `xadmin_log_user_id_bb16a176_fk_users_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 102 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of xadmin_log
-- ----------------------------
INSERT INTO `xadmin_log` VALUES (1, '2019-04-04 10:44:37.782665', '127.0.0.1', '1', 'EmailVerifyRecord object', 'create', '已添加', 8, 1);
INSERT INTO `xadmin_log` VALUES (2, '2019-04-04 10:48:21.024433', '127.0.0.1', NULL, '', 'delete', '批量删除 1 个 邮箱验证码', NULL, 1);
INSERT INTO `xadmin_log` VALUES (3, '2019-04-04 10:48:40.615554', '127.0.0.1', '2', 'EmailVerifyRecord object', 'create', '已添加', 8, 1);
INSERT INTO `xadmin_log` VALUES (4, '2019-04-04 10:51:41.343891', '127.0.0.1', NULL, '', 'delete', '批量删除 1 个 邮箱验证码', NULL, 1);
INSERT INTO `xadmin_log` VALUES (5, '2019-04-04 10:52:23.285290', '127.0.0.1', '3', 'EmailVerifyRecord object', 'create', '已添加', 8, 1);
INSERT INTO `xadmin_log` VALUES (6, '2019-04-04 11:01:55.657028', '127.0.0.1', '4', 'EmailVerifyRecord object', 'create', '已添加', 8, 1);
INSERT INTO `xadmin_log` VALUES (7, '2019-04-04 11:02:40.531594', '127.0.0.1', '5', 'EmailVerifyRecord object', 'create', '已添加', 8, 1);
INSERT INTO `xadmin_log` VALUES (8, '2019-04-04 11:05:34.486544', '127.0.0.1', '6', 'EmailVerifyRecord object', 'create', '已添加', 8, 1);
INSERT INTO `xadmin_log` VALUES (9, '2019-04-04 11:06:39.867284', '127.0.0.1', NULL, '', 'delete', '批量删除 4 个 邮箱验证码', NULL, 1);
INSERT INTO `xadmin_log` VALUES (10, '2019-04-04 11:07:00.008436', '127.0.0.1', '7', '12345(nihao@qq.com)', 'create', '已添加', 8, 1);
INSERT INTO `xadmin_log` VALUES (11, '2019-04-04 11:07:09.117957', '127.0.0.1', '7', '12345(nihao@qq.com)', 'change', '没有字段被修改。', 8, 1);
INSERT INTO `xadmin_log` VALUES (12, '2019-04-04 11:10:42.867182', '127.0.0.1', '8', 'admin(123@qq.com)', 'create', '已添加', 8, 1);
INSERT INTO `xadmin_log` VALUES (13, '2019-05-07 17:13:41.441332', '127.0.0.1', '1', 'CityDict object', 'create', '已添加', 10, 5);
INSERT INTO `xadmin_log` VALUES (14, '2019-05-07 17:13:55.458133', '127.0.0.1', '2', 'CityDict object', 'create', '已添加', 10, 5);
INSERT INTO `xadmin_log` VALUES (15, '2019-05-07 17:14:11.247037', '127.0.0.1', '3', 'CityDict object', 'create', '已添加', 10, 5);
INSERT INTO `xadmin_log` VALUES (16, '2019-05-07 17:14:36.949507', '127.0.0.1', '4', 'CityDict object', 'create', '已添加', 10, 5);
INSERT INTO `xadmin_log` VALUES (17, '2019-05-07 17:15:54.132921', '127.0.0.1', '5', '蔡家坡', 'create', '已添加', 10, 5);
INSERT INTO `xadmin_log` VALUES (18, '2019-05-07 17:20:10.132564', '127.0.0.1', '1', 'CourseOrg object', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (19, '2019-05-07 17:22:32.895729', '127.0.0.1', '2', '达内教育', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (20, '2019-05-07 17:23:40.837615', '127.0.0.1', '3', '千峰教育', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (21, '2019-05-07 17:26:19.959716', '127.0.0.1', '4', '爱数圈', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (22, '2019-05-07 17:27:29.951720', '127.0.0.1', '5', '懂球帝', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (23, '2019-05-07 17:28:46.755113', '127.0.0.1', '6', '北京大学', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (24, '2019-05-07 17:29:54.829006', '127.0.0.1', '7', '清华大学', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (25, '2019-05-07 17:31:46.110371', '127.0.0.1', '8', '西安交通大学', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (26, '2019-05-07 17:33:18.341647', '127.0.0.1', '9', '斯坦福大学', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (27, '2019-05-07 17:35:22.381741', '127.0.0.1', '10', '北京石油化工学院', 'create', '已添加', 11, 5);
INSERT INTO `xadmin_log` VALUES (28, '2019-05-08 14:29:11.317574', '127.0.0.1', '1', 'Teacher object', 'create', '已添加', 12, 5);
INSERT INTO `xadmin_log` VALUES (29, '2019-05-08 14:30:42.890811', '127.0.0.1', '2', '詹姆', 'create', '已添加', 12, 5);
INSERT INTO `xadmin_log` VALUES (30, '2019-05-08 14:32:02.402359', '127.0.0.1', '3', '夜王', 'create', '已添加', 12, 5);
INSERT INTO `xadmin_log` VALUES (31, '2019-05-08 14:32:28.447849', '127.0.0.1', '4', '小马哥', 'create', '已添加', 12, 5);
INSERT INTO `xadmin_log` VALUES (32, '2019-05-08 14:32:56.111431', '127.0.0.1', '5', '团团', 'create', '已添加', 12, 5);
INSERT INTO `xadmin_log` VALUES (33, '2019-05-08 14:33:45.295244', '127.0.0.1', '6', '施一公', 'create', '已添加', 12, 5);
INSERT INTO `xadmin_log` VALUES (34, '2019-05-08 14:34:23.026402', '127.0.0.1', '7', '王琪', 'create', '已添加', 12, 5);
INSERT INTO `xadmin_log` VALUES (35, '2019-05-08 15:02:01.231246', '127.0.0.1', '1', 'django入门', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (36, '2019-05-08 17:35:02.262371', '127.0.0.1', '7', '王琪', 'change', '已修改 image 。', 12, 5);
INSERT INTO `xadmin_log` VALUES (37, '2019-05-08 17:35:15.488128', '127.0.0.1', '6', '施一公', 'change', '已修改 image 。', 12, 5);
INSERT INTO `xadmin_log` VALUES (38, '2019-05-08 17:35:21.899494', '127.0.0.1', '5', '团团', 'change', '已修改 image 。', 12, 5);
INSERT INTO `xadmin_log` VALUES (39, '2019-05-08 17:35:28.629879', '127.0.0.1', '4', '小马哥', 'change', '已修改 image 。', 12, 5);
INSERT INTO `xadmin_log` VALUES (40, '2019-05-08 17:35:35.003244', '127.0.0.1', '3', '夜王', 'change', '已修改 image 。', 12, 5);
INSERT INTO `xadmin_log` VALUES (41, '2019-05-08 17:35:42.022645', '127.0.0.1', '2', '詹姆', 'change', '已修改 image 。', 12, 5);
INSERT INTO `xadmin_log` VALUES (42, '2019-05-08 17:35:49.686084', '127.0.0.1', '1', '史塔克', 'change', '已修改 image 。', 12, 5);
INSERT INTO `xadmin_log` VALUES (43, '2019-05-08 17:47:52.418422', '127.0.0.1', '1', 'django入门', 'change', '已修改 course_org 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (44, '2019-05-08 17:47:58.405764', '127.0.0.1', '1', 'django入门', 'change', '没有字段被修改。', 13, 5);
INSERT INTO `xadmin_log` VALUES (45, '2019-05-08 17:48:15.151722', '127.0.0.1', '1', 'django入门', 'change', '没有字段被修改。', 13, 5);
INSERT INTO `xadmin_log` VALUES (46, '2019-05-08 21:16:15.753572', '127.0.0.1', '8', '牛犇', 'create', '已添加', 12, 5);
INSERT INTO `xadmin_log` VALUES (47, '2019-05-16 20:17:12.860101', '127.0.0.1', '2', '爬虫', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (48, '2019-05-16 20:17:59.225753', '127.0.0.1', '3', '嵌入式', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (49, '2019-05-16 20:18:34.464769', '127.0.0.1', '4', '七天学会python', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (50, '2019-05-16 20:19:06.123580', '127.0.0.1', '5', '足球的自我修养', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (51, '2019-05-16 20:19:48.402998', '127.0.0.1', '6', '北京大学发展史', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (52, '2019-05-16 20:20:24.373055', '127.0.0.1', '7', 'numpy 的概述', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (53, '2019-05-16 20:21:04.106328', '127.0.0.1', '8', '我们都是西安交通大学毕业的。', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (54, '2019-05-16 20:21:24.186476', '127.0.0.1', '8', '西安交大最牛逼的课程。', 'change', '已修改 name 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (55, '2019-05-16 20:22:10.122104', '127.0.0.1', '9', 'pandas', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (56, '2019-05-16 20:22:52.361520', '127.0.0.1', '10', '石油冶炼', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (57, '2019-05-16 21:10:59.782671', '127.0.0.1', '3', '嵌入式', 'change', '没有字段被修改。', 13, 5);
INSERT INTO `xadmin_log` VALUES (58, '2019-05-17 17:11:07.832647', '127.0.0.1', '1', 'UserCourse object', 'create', '已添加', 21, 5);
INSERT INTO `xadmin_log` VALUES (59, '2019-05-17 17:11:19.473313', '127.0.0.1', '2', 'UserCourse object', 'create', '已添加', 21, 5);
INSERT INTO `xadmin_log` VALUES (60, '2019-05-17 17:11:33.966142', '127.0.0.1', '3', 'UserCourse object', 'create', '已添加', 21, 5);
INSERT INTO `xadmin_log` VALUES (61, '2019-05-17 18:09:29.099908', '127.0.0.1', '4', '七天学会python', 'change', '已修改 tag 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (62, '2019-05-17 18:09:36.697343', '127.0.0.1', '2', '爬虫', 'change', '已修改 tag 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (63, '2019-05-17 18:09:44.733802', '127.0.0.1', '10', '石油冶炼', 'change', '已修改 tag 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (64, '2019-05-18 16:00:51.388449', '127.0.0.1', '1', '中国足球', 'create', '已添加', 14, 5);
INSERT INTO `xadmin_log` VALUES (65, '2019-05-18 16:01:03.643150', '127.0.0.1', '2', '国际足球', 'create', '已添加', 14, 5);
INSERT INTO `xadmin_log` VALUES (66, '2019-05-18 16:01:15.328818', '127.0.0.1', '3', '辣鸡足球', 'create', '已添加', 14, 5);
INSERT INTO `xadmin_log` VALUES (67, '2019-05-18 16:05:35.150679', '127.0.0.1', '1', '搞笑的中国足球', 'create', '已添加', 15, 5);
INSERT INTO `xadmin_log` VALUES (68, '2019-05-18 16:08:58.770326', '127.0.0.1', '1', '搞笑的中国足球', 'change', '已修改 url 。', 15, 5);
INSERT INTO `xadmin_log` VALUES (69, '2019-05-18 16:09:28.411021', '127.0.0.1', '2', '这是一个外部跳转的视频', 'create', '已添加', 15, 5);
INSERT INTO `xadmin_log` VALUES (70, '2019-05-18 16:09:40.269699', '127.0.0.1', '3', '垃圾足球', 'create', '已添加', 15, 5);
INSERT INTO `xadmin_log` VALUES (71, '2019-05-25 11:28:40.017785', '127.0.0.1', '3', 'UserCourse object', 'change', '没有字段被修改。', 21, 5);
INSERT INTO `xadmin_log` VALUES (72, '2019-05-25 11:43:00.003973', '127.0.0.1', '6', '北京大学发展史', 'change', '已修改 tag 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (73, '2019-05-25 11:43:12.126666', '127.0.0.1', '9', 'pandas', 'change', '已修改 tag 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (74, '2019-05-25 11:43:20.065120', '127.0.0.1', '3', '嵌入式', 'change', '已修改 tag 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (75, '2019-05-25 11:45:58.383176', '127.0.0.1', '1', 'django入门', 'change', '已修改 tag 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (76, '2019-05-25 12:37:36.888400', '127.0.0.1', '4', '第一章 石油简书', 'create', '已添加', 14, 5);
INSERT INTO `xadmin_log` VALUES (77, '2019-05-25 12:37:49.676132', '127.0.0.1', '4', '第一章 石油简述', 'change', '已修改 name 。', 14, 5);
INSERT INTO `xadmin_log` VALUES (78, '2019-05-25 12:38:01.339799', '127.0.0.1', '5', '第二章 石油冶炼', 'create', '已添加', 14, 5);
INSERT INTO `xadmin_log` VALUES (79, '2019-05-25 12:38:16.643674', '127.0.0.1', '6', '第三章 石油提取', 'create', '已添加', 14, 5);
INSERT INTO `xadmin_log` VALUES (80, '2019-05-25 12:39:39.033386', '127.0.0.1', '4', '我们的时代', 'create', '已添加', 15, 5);
INSERT INTO `xadmin_log` VALUES (81, '2019-05-25 12:40:34.382552', '127.0.0.1', '5', '2.1 石油的好处', 'create', '已添加', 15, 5);
INSERT INTO `xadmin_log` VALUES (82, '2019-05-25 12:40:46.856266', '127.0.0.1', '4', '我们的时代', 'change', '没有字段被修改。', 15, 5);
INSERT INTO `xadmin_log` VALUES (83, '2019-05-25 12:54:43.278106', '127.0.0.1', '1', '如何提炼石油', 'create', '已添加', 16, 5);
INSERT INTO `xadmin_log` VALUES (84, '2019-05-25 13:09:43.588601', '127.0.0.1', '10', '石油冶炼', 'change', '已修改 teacher 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (85, '2019-05-25 13:35:18.887415', '127.0.0.1', '10', '石油冶炼', 'change', '已修改 youneed_konw 和 teacher_tell 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (86, '2019-05-25 17:36:12.605503', '127.0.0.1', '2', '如何磨洋工', 'create', '已添加', 16, 5);
INSERT INTO `xadmin_log` VALUES (87, '2019-05-31 22:37:17.671743', '127.0.0.1', '1', 'UserMessage object', 'create', '已添加', 20, 5);
INSERT INTO `xadmin_log` VALUES (88, '2019-06-01 00:33:14.781667', '127.0.0.1', '1', 'Banner object', 'create', '已添加', 9, 5);
INSERT INTO `xadmin_log` VALUES (89, '2019-06-01 00:33:40.524140', '127.0.0.1', '2', 'Banner object', 'create', '已添加', 9, 5);
INSERT INTO `xadmin_log` VALUES (90, '2019-06-01 00:33:58.382161', '127.0.0.1', '3', 'Banner object', 'create', '已添加', 9, 5);
INSERT INTO `xadmin_log` VALUES (91, '2019-06-01 00:34:13.632033', '127.0.0.1', '4', 'Banner object', 'create', '已添加', 9, 5);
INSERT INTO `xadmin_log` VALUES (92, '2019-06-01 00:34:31.774071', '127.0.0.1', '5', 'Banner object', 'create', '已添加', 9, 5);
INSERT INTO `xadmin_log` VALUES (93, '2019-06-02 10:40:54.308139', '127.0.0.1', '2', '842549758@qq.com', 'change', '已修改 last_login，is_staff，nick_name，birthday，address 和 mobile 。', 7, 5);
INSERT INTO `xadmin_log` VALUES (94, '2019-06-02 10:42:11.297542', '127.0.0.1', '2', '842549758@qq.com', 'change', '已修改 last_login 和 user_permissions 。', 7, 5);
INSERT INTO `xadmin_log` VALUES (95, '2019-06-02 10:46:42.263041', '127.0.0.1', '1', '编辑部门', 'create', '已添加', 3, 5);
INSERT INTO `xadmin_log` VALUES (96, '2019-06-02 10:48:11.666154', '127.0.0.1', '2', '842549758@qq.com', 'change', '已修改 last_login 和 groups 。', 7, 5);
INSERT INTO `xadmin_log` VALUES (97, '2019-06-02 11:20:03.519506', '127.0.0.1', '11', 'web前端课程', 'create', '已添加', 13, 5);
INSERT INTO `xadmin_log` VALUES (98, '2019-06-02 14:03:52.632392', '127.0.0.1', '5', '足球的自我修养', 'change', '已修改 is_banner，tag，youneed_konw 和 teacher_tell 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (99, '2019-06-02 14:04:16.791774', '127.0.0.1', '11', 'web前端课程', 'change', '已修改 is_banner 。', 13, 5);
INSERT INTO `xadmin_log` VALUES (100, '2019-06-02 14:34:02.509911', '127.0.0.1', '10', '北京石油化工学院', 'change', '没有字段被修改。', 11, 5);
INSERT INTO `xadmin_log` VALUES (101, '2019-06-02 14:35:19.666325', '127.0.0.1', '5', '足球的自我修养', 'change', '没有字段被修改。', 27, 5);

-- ----------------------------
-- Table structure for xadmin_usersettings
-- ----------------------------
DROP TABLE IF EXISTS `xadmin_usersettings`;
CREATE TABLE `xadmin_usersettings`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `xadmin_usersettings_user_id_edeabe4a_fk_users_userprofile_id`(`user_id`) USING BTREE,
  CONSTRAINT `xadmin_usersettings_user_id_edeabe4a_fk_users_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of xadmin_usersettings
-- ----------------------------
INSERT INTO `xadmin_usersettings` VALUES (1, 'dashboard:home:pos', '', 1);
INSERT INTO `xadmin_usersettings` VALUES (2, 'site-theme', 'https://bootswatch.com/3/lumen/bootstrap.min.css', 1);
INSERT INTO `xadmin_usersettings` VALUES (3, 'dashboard:home:pos', '', 5);
INSERT INTO `xadmin_usersettings` VALUES (4, 'site-theme', 'https://bootswatch.com/3/lumen/bootstrap.min.css', 5);
INSERT INTO `xadmin_usersettings` VALUES (5, 'dashboard:home:pos', '', 2);
INSERT INTO `xadmin_usersettings` VALUES (6, 'courses_course_editform_portal', 'box-0,lesson_set-group,,coursesource_set-group', 5);

-- ----------------------------
-- Table structure for xadmin_userwidget
-- ----------------------------
DROP TABLE IF EXISTS `xadmin_userwidget`;
CREATE TABLE `xadmin_userwidget`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `page_id` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `widget_type` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `xadmin_userwidget_user_id_c159233a_fk_users_userprofile_id`(`user_id`) USING BTREE,
  CONSTRAINT `xadmin_userwidget_user_id_c159233a_fk_users_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `users_userprofile` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
