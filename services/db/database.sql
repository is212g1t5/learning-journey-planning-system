-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 30, 2022 at 11:27 PM
-- Server version: 8.0.21
-- PHP Version: 7.4.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+08:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ljps`
--
DROP DATABASE IF EXISTS `ljps`;
CREATE DATABASE IF NOT EXISTS `ljps` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `ljps`;

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
CREATE TABLE IF NOT EXISTS `courses` (
  `course_id` int NOT NULL,
  `course_name` varchar(50) NOT NULL,
  `course_desc` varchar(255) NOT NULL,
  `course_status` tinyint(1) NOT NULL,
  `course_type` varchar(10) NOT NULL,
  `course_category` varchar(50) NOT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
CREATE TABLE IF NOT EXISTS `groups` (
  `group_id` int NOT NULL AUTO_INCREMENT,
  `group_name` varchar(20) NOT NULL,
  PRIMARY KEY (`group_id`),
  UNIQUE KEY `group_name` (`group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

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

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`, `role_desc`, `role_status`, `role_sector`, `role_track`) VALUES
(1, 'Designer', 'The Designer (Engineering Design) develops technical drawings and models based on pre-defined specifications and engineering calculations. He/She interprets engineering calculations and uses design software and modelling methods for preparation of drawings and designs. He identifies relevant design data and highlights design issues where applicable. He also complies with Design for Safety (DfS) regulations and ensures compliance with industry standards and international conventions. He possesses high detail', 1, 'Engineering Services', 'Engineering Design'),
(2, 'Chief Executive Officer/Managing Director/General Manager/Presid', 'The Chief Executive Officer/Chief Operating Officer/Managing Director/General Manager/President defines the long-term strategic direction to grow the business in line with the organisation’s overall vision, mission and values. He/She translates broad goals into achievable steps, anticipates and stays ahead of trends, and takes advantage of business opportunities. He represents the organisation with customers, investors, and business partners, and holds responsibility for fostering a culture of workplace saf', 1, 'Engineering Services ', 'General Management ');

-- --------------------------------------------------------

--
-- Table structure for table `skills`
--

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

--
-- Dumping data for table `skills`
--

INSERT INTO `skills` (`skill_id`, `skill_name`, `skill_category`, `skill_desc`, `skill_status`) VALUES
(1, 'Creative Thinking', 'Thinking Critically', 'Adopt diverse perspectives in combining ideas or information and making connections between different fields to create different ideas, improvements and solutions', 1),
(2, 'Front-End Engineering and Design', 'Engineering Design Management\r\n', 'Manage Front-End Engineering and Design for equipment, components and systems', 1),
(3, '3D Modelling', 'Engineering Design Management', 'Generate 3D models using a variety of modelling software to represent characteristics of a real-world system', 1);

-- --------------------------------------------------------

--
-- Table structure for table `staffs`
--

DROP TABLE IF EXISTS `staffs`;
CREATE TABLE IF NOT EXISTS `staffs` (
  `staff_id` int NOT NULL,
  `staff_fname` varchar(50) NOT NULL,
  `staff_lname` varchar(50) NOT NULL,
  `dept` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `user_group` int NOT NULL,
  PRIMARY KEY (`staff_id`),
  KEY `group_FK` (`user_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `staffs`
--
ALTER TABLE `staffs`
  ADD CONSTRAINT `group_FK` FOREIGN KEY (`user_group`) REFERENCES `groups` (`group_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

-- 
-- Table structure for `learning_journeys`
--
DROP TABLE IF EXISTS `learning_journeys`;
CREATE TABLE IF NOT EXISTS `learning_journeys` (
  `learning_journey_id` int NOT NULL auto_increment,
  `learning_journey_name` varchar(50) NOT NULL unique,
  `staff_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`learning_journey_id`),
  constraint lj_fk1 FOREIGN KEY(staff_id) references staffs(staff_id),
  constraint lj_fk2 FOREIGN KEY(role_id) references roles(role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 
-- Table structure for `learning_journey_courses`
--
DROP TABLE IF EXISTS `learning_journey_courses`;
CREATE TABLE IF NOT EXISTS `learning_journey_courses` (
  `learning_journey_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`learning_journey_id`,`course_id`),
  constraint lc_fk1 FOREIGN KEY(course_id) references courses(course_id),
  constraint lc_fk2 FOREIGN KEY(learning_journey_id) references learning_journeys(learning_journey_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 
-- Table structure for `learning_journey_skills`
--
DROP TABLE IF EXISTS `learning_journey_skills`;
CREATE TABLE IF NOT EXISTS `learning_journey_skills` (
  `learning_journey_id` int NOT NULL,
  `skill_id` int NOT NULL,
  PRIMARY KEY (`learning_journey_id`,`skill_id`),
  constraint ls_fk1 FOREIGN KEY(skill_id) references skills(skill_id),
  constraint ls_fk2 FOREIGN KEY(learning_journey_id) references learning_journeys(learning_journey_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 
-- Table structure for `learning_journey_roles`
--
DROP TABLE IF EXISTS `learning_journey_roles`;
CREATE TABLE IF NOT EXISTS `learning_journey_roles` (
  `learning_journey_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`learning_journey_id`,`role_id`),
  constraint lr_fk1 FOREIGN KEY(role_id) references roles(role_id),
  constraint lr_fk2 FOREIGN KEY(learning_journey_id) references learning_journeys(learning_journey_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 
-- Table structure for `skills_courses`
--
DROP TABLE IF EXISTS `skills_courses`;
CREATE TABLE IF NOT EXISTS `skills_courses` (
  `skill_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`skill_id`,`course_id`),
  FOREIGN KEY (`skill_id`) REFERENCES skills(`skill_id`),
  FOREIGN KEY (`course_id`) REFERENCES courses(`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 
-- Table structure for `skills_roles`
--
DROP TABLE IF EXISTS `skills_roles`;
CREATE TABLE IF NOT EXISTS `skills_roles` (
  `skill_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`skill_id`,`role_id`),
  FOREIGN KEY (`skill_id`) REFERENCES skills(`skill_id`),
  FOREIGN KEY (`role_id`) REFERENCES roles(`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
