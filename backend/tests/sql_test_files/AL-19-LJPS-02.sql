DROP TABLE IF EXISTS `skills_roles`;
DROP TABLE IF EXISTS `lj_roles`;
DROP TABLE IF EXISTS `lj_role_skill`;
DROP TABLE IF EXISTS `lj_courses`;
DROP TABLE IF EXISTS `learning_journeys`;
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


INSERT INTO `roles` (`role_id`, `role_name`, `role_desc`, `role_status`, `role_sector`, `role_track`) VALUES
(1, 'Designer', 'The Designer (Engineering Design) develops technical drawings and models based on pre-defined specifications and engineering calculations. He/She interprets engineering calculations and uses design software and modelling methods for preparation of drawings and designs. He identifies relevant design data and highlights design issues where applicable. He also complies with Design for Safety (DfS) regulations and ensures compliance with industry standards and international conventions. He possesses high detail', 1, 'Engineering Services', 'Engineering Design'),
(2, 'Chief Executive Officer/Managing Director/General Manager', 'The Chief Executive Officer/Chief Operating Officer/Managing Director/General Manager defines the long-term strategic direction to grow the business in line with the organisation’s overall vision, mission and values. He/She translates broad goals into achievable steps, anticipates and stays ahead of trends, and takes advantage of business opportunities. He represents the organisation with customers, investors, and business partners, and holds responsibility for fostering a culture of workplace safety', 1, 'Engineering Services ', 'General Management '),
(11, 'Director', "The Director (Project Financing) is responsible for spearheading the project\r\nfinancing activities while ensuring alignment with the organization\'s financing\r\ngoals. He drives direction and strategy for project financing scoping,\r\nvaluation analysis and delivery. He is responsible for origination of project\r\nfinancing, and maintains strong links to external stakeholders. He serves as\r\nan advisor to clients and stakeholders on project strategy and establishes\r\nstrong rapport to enhance customer satisfaction.", 0, 'Engineering Services', 'Project Financing')
