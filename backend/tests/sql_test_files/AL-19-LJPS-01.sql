DROP TABLE IF EXISTS `skills_roles`;
DROP TABLE IF EXISTS `lj_roles`;
DROP TABLE IF EXISTS `roles`;


CREATE TABLE IF NOT EXISTS `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(64) NOT NULL,
  `role_desc` varchar(512) NOT NULL,
  `role_status` tinyint(1) NOT NULL,
  `role_sector` varchar(64) NOT NULL,
  `role_track` varchar(64) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `skills_roles`;
CREATE TABLE IF NOT EXISTS `skills_roles` (
  `skill_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`skill_id`,`role_id`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `lj_roles`;
CREATE TABLE IF NOT EXISTS `lj_roles` (
  `learning_journey_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`learning_journey_id`,`role_id`),
  KEY `lr_fk1` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;