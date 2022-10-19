DROP TABLE IF EXISTS `skills_courses`;
DROP TABLE IF EXISTS `lj_courses`;
DROP TABLE IF EXISTS `registration`;
DROP TABLE IF EXISTS `courses`;




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
('FIN003', 'Business Continuity Planning', 'Business continuity planning is essential in any business to minimise loss when faced with potential threats and disruptions.', 0, 'External', 'Finance');

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
(3, 'COR001');

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