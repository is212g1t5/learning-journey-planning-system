DROP TABLE IF EXISTS `lj_skills`;
DROP TABLE IF EXISTS `lj_courses`;
DROP TABLE IF EXISTS `registration`;
DROP TABLE IF EXISTS `skills_roles`;
DROP TABLE IF EXISTS `skills_courses`;
DROP TABLE IF EXISTS `courses`;
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
(2, 'Front-End Engineering and Design', 'Engineering Design Management\r\n', 'Manage Front-End Engineering and Design for equipment, components and systems', 1),
(3, '3D Modelling', 'Engineering Design Management', 'Generate 3D models using a variety of modelling software to represent characteristics of a real-world system', 1);

CREATE TABLE IF NOT EXISTS `courses` (
  `course_id` varchar(20) NOT NULL,
  `course_name` varchar(50) NOT NULL,
  `course_desc` varchar(255) NOT NULL,
  `course_status` int NOT NULL,
  `course_type` varchar(10) NOT NULL,
  `course_category` varchar(50) NOT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `courses` (`course_id`, `course_name`, `course_desc`, `course_status`, `course_type`, `course_category`) VALUES
('COR001', 'Systems Thinking and Design', 'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,', 1, 'Internal', 'Core'),
('FIN002', 'Risk and Compliance Reporting', 'Regulatory reporting is a requirement for businesses from highly regulated sectors to demonstrate compliance with the necessary regulatory provisions.', 1, 'External', 'Finance'),
('FIN003', 'Business Continuity Planning', 'Business continuity planning is essential in any business to minimise loss when faced with potential threats and disruptions.', 0, 'External', 'Finance'),
('MGT001', 'People Management', 'enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.', 1, 'Internal', 'Management'),
('SAL004', 'Stakeholder Management', 'Develop a stakeholder engagement plan and negotiate with stakeholders to arrive at mutually-beneficial arrangements.', 1, 'Internal', 'Sales');

DROP TABLE IF EXISTS `lj_courses`;
CREATE TABLE IF NOT EXISTS `lj_courses` (
  `learning_journey_id` int NOT NULL,
  `course_id` varchar(20) NOT NULL,
  PRIMARY KEY (`learning_journey_id`,`course_id`),
  KEY `lc_fk1` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `skills_courses`;
CREATE TABLE IF NOT EXISTS `skills_courses` (
  `skill_id` int NOT NULL,
  `course_id` varchar(20) NOT NULL,
  PRIMARY KEY (`skill_id`,`course_id`),
  KEY `course_id` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO skills_courses (skill_id, course_id) VALUES
(1, 'FIN003'),
(2, 'FIN002'),
(3, 'COR001'),
(2, 'FIN003');

CREATE TABLE IF NOT EXISTS `lj_skills` (
  `learning_journey_id` int NOT NULL,
  `skill_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`learning_journey_id`,`skill_id`,`role_id`),
  KEY `ls_fk1` (`skill_id`),
  KEY `ls_fk2` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `lj_skills`
  ADD CONSTRAINT `ls_fk1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`skill_id`),
  ADD CONSTRAINT `ls_fk2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`),
  ADD CONSTRAINT `ls_fk3` FOREIGN KEY (`learning_journey_id`) REFERENCES `learning_journeys` (`learning_journey_id`);

CREATE TABLE IF NOT EXISTS `skills_roles` (
  `skill_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`skill_id`,`role_id`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `skills_roles`
  ADD CONSTRAINT `skills_roles_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`skill_id`),
  ADD CONSTRAINT `skills_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`);

CREATE TABLE IF NOT EXISTS `lj_courses` (
  `learning_journey_id` int NOT NULL,
  `course_id` varchar(20) NOT NULL,
  PRIMARY KEY (`learning_journey_id`,`course_id`),
  KEY `lc_fk1` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `lj_courses`
  ADD CONSTRAINT `lc_fk1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  ADD CONSTRAINT `lc_fk2` FOREIGN KEY (`learning_journey_id`) REFERENCES `learning_journeys` (`learning_journey_id`);

CREATE TABLE IF NOT EXISTS `registration` (
  `reg_id` int NOT NULL,
  `course_id` varchar(20) NOT NULL,
  `staff_id` int NOT NULL,
  `reg_status` varchar(11) NOT NULL,
  `completion_status` varchar(20) NOT NULL,
  PRIMARY KEY (`reg_id`),
  KEY `course_id` (`course_id`),
  KEY `staff_id` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

ALTER TABLE `registration`
  ADD CONSTRAINT `registration_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  ADD CONSTRAINT `registration_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `staffs` (`staff_id`);
