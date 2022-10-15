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
(2, 'Chief Executive Officer/Managing Director/General Manager/Presid', 'The Chief Executive Officer/Chief Operating Officer/Managing Director/General Manager/President defines the long-term strategic direction to grow the business in line with the organisation’s overall vision, mission and values. He/She translates broad goals into achievable steps, anticipates and stays ahead of trends, and takes advantage of business opportunities. He represents the organisation with customers, investors, and business partners, and holds responsibility for fostering a culture of workplace saf', 1, 'Engineering Services ', 'General Management ');