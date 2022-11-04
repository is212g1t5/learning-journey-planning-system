DROP TABLE IF EXISTS `skills`;

CREATE TABLE IF NOT EXISTS `skills` (
  `skill_id` int NOT NULL AUTO_INCREMENT,
  `skill_name` varchar(64) NOT NULL,
  `skill_category` varchar(64) NOT NULL,
  `skill_desc` varchar(512) NOT NULL,
  `skill_status` tinyint(1) NOT NULL,
  PRIMARY KEY (`skill_id`),
  UNIQUE KEY `skill_name` (`skill_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `skills` (`skill_id`, `skill_name`, `skill_category`, `skill_desc`, `skill_status`) VALUES
(1, 'Creative Thinking', 'Thinking Critically', 'Adopt diverse perspectives in combining ideas or information and making connections between different fields to create different ideas, improvements and solutions', 1),
(2, 'Front-End Engineering and Design', 'Engineering Design Management\r\n', 'Manage Front-End Engineering and Design for equipment, components and systems', 1);
