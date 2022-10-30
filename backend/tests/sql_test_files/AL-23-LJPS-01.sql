-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Oct 27, 2022 at 06:52 AM
-- Server version: 8.0.31
-- PHP Version: 8.0.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


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
-- Table structure for table `skills_courses`
--

DROP TABLE IF EXISTS `skills_courses`;
CREATE TABLE `skills_courses` (
  `skill_id` int NOT NULL,
  `course_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `skills_courses`
--

INSERT INTO `skills_courses` (`skill_id`, `course_id`) VALUES
(1, 'COR001'),
(2, 'COR001'),
(2, 'COR002'),
(4, 'FIN001'),
(9, 'FIN001'),
(5, 'SAL001'),
(9, 'SAL001'),
(10, 'SAL001');

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
  `course_id` varchar(20) NOT NULL,
  `course_name` varchar(50) NOT NULL,
  `course_desc` varchar(255) NOT NULL,
  `course_status` int NOT NULL,
  `course_type` varchar(10) NOT NULL,
  `course_category` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`course_id`, `course_name`, `course_desc`, `course_status`, `course_type`, `course_category`) VALUES
('COR001', 'Systems Thinking and Design', 'This foundation module aims to introduce students to the fundamental concepts and underlying principles of systems thinking,', 1, 'Internal', 'Core'),
('COR002', 'Lean Six Sigma Green Belt Certification', 'Apply Lean Six Sigma methodology and statistical tools such as Minitab to be used in process analytics', 1, 'Internal', 'Core'),
('COR004', 'Service Excellence', 'The programme provides the learner with the key foundations of what builds customer confidence in the service industr', -1, 'Internal', 'Core'),
('COR006', 'Manage Change', 'Identify risks associated with change and develop risk mitigation plans.', 0, 'External', 'Core'),
('FIN001', 'Data Collection and Analysis', 'Data is meaningless unless insights and analysis can be drawn to provide useful information for business decision-making. It is imperative that data quality, integrity and security ', 1, 'External', 'Finance'),
('FIN002', 'Risk and Compliance Reporting', 'Regulatory reporting is a requirement for businesses from highly regulated sectors to demonstrate compliance with the necessary regulatory provisions.', 1, 'External', 'Finance'),
('FIN003', 'Business Continuity Planning', 'Business continuity planning is essential in any business to minimise loss when faced with potential threats and disruptions.', 0, 'External', 'Finance'),
('HRD001', 'Leading and Shaping a Culture in Learning', 'This training programme, delivered by the National Centre of Excellence (Workplace Learning), aims to equip participants with the skills and knowledge of the National workplace learning certification framework,', 1, 'External', 'HR'),
('MGT001', 'People Management', 'enable learners to manage team performance and development through effective communication, conflict resolution and negotiation skills.', 1, 'Internal', 'Management'),
('MGT002', 'Workplace Conflict Management for Professionals', 'This course will address the gaps to build consensus and utilise knowledge of conflict management techniques to diffuse tensions and achieve resolutions effectively in the best interests of the organisation.', 1, 'External', 'Management'),
('MGT003', 'Enhance Team Performance Through Coaching', 'The course aims to upskill real estate team leaders in the area of service coaching for performance.', -1, 'Internal', 'Management'),
('MGT004', 'Personal Effectiveness for Leaders', 'Learners will be able to acquire the skills and knowledge to undertake self-assessment in relation to one', 1, 'External', 'Management'),
('MGT007', 'Supervisory Management Skills', 'Supervisors lead teams, manage tasks, solve problems, report up and down the hierarchy, and much more. ', 0, 'External', 'Management'),
('SAL001', 'Risk Management for Smart Business', 'Apply risk management concepts to digital business', 0, 'Internal', 'Sales'),
('SAL002', 'CoC in Smart Living Solutions', 'Participants will acquire the knowledge and skills in setting up a smart living solution', -1, 'External', 'Sales'),
('SAL003', 'Optimising Your Brand For The Digital Spaces', 'Digital has fundamentally shifted communication between brands and their consumers from a one-way broadcast to a two-way dialogue. In a hastened bid to transform their businesses to be digital market-ready,', 1, 'External', 'Sales'),
('SAL004', 'Stakeholder Management', 'Develop a stakeholder engagement plan and negotiate with stakeholders to arrive at mutually-beneficial arrangements.', 1, 'Internal', 'Sales'),
('tch001', 'Print Server Setup', 'Setting up print server in enterprise environment', 0, 'Internal', 'Technical'),
('tch002', 'Canon MFC Setup', 'Setting up Canon ImageRUNNER series of products', 0, 'Internal', 'Technical'),
('tch003', 'Canon MFC Mainteance and Troubleshooting', 'Troubleshoot and fixing L2,3 issues of Canon ImageRUNNER series of products', 1, 'Internal', 'Technical'),
('tch004', 'Introduction to Open Platform Communications', 'This course provides the participants with a good in-depth understanding of the SS IEC 62541 standard', -1, 'Internal', 'Technical'),
('tch005', 'An Introduction to Sustainability', 'The course provides learners with the multi-faceted basic knowledge of sustainability.', 1, 'External', 'Technical'),
('tch006', 'Machine Learning DevOps Engineer', 'The Machine Learning DevOps Engineer Nanodegree program focuses on the software engineering fundamentals needed to successfully streamline the deployment of data and machine-learning models', -1, 'Internal', 'Technical'),
('tch008', 'Technology Intelligence and Strategy', 'Participants will be able to gain knowledge and skills on: - establishing technology strategy with technology intelligence framework and tools', 1, 'External', 'Technical'),
('tch009', 'Smart Sensing Technology', 'This course introduces sensors and sensing systems. The 5G infrastructure enables the many fast-growing IoT applications equipped with sensors ', -1, 'External', 'Technical'),
('tch012', 'Internet of Things', 'The Internet of Things (IoT) is integrating our digital and physical world, opening up new and exciting opportunities to deploy, automate, optimize and secure diverse use cases and applications. ', 1, 'Internal', 'Technical'),
('tch013', 'Managing Cybersecurity and Risks', 'Digital security is the core of our daily lives considering that our dependence on the digital world', 1, 'Internal', 'Technical'),
('tch014', 'Certified Information Privacy Professional', 'The Certified Information Privacy Professional/ Asia (CIPP/A) is the first publicly available privacy certification', 1, 'External', 'Technical'),
('tch015', 'Network Security', 'Understanding of the fundamental knowledge of network security including cryptography, authentication and key distribution. The security techniques at various layers of computer networks are examined.', 1, 'External', 'Technical'),
('tch018', 'Professional Project Management', 'solid foundation in the project management processes from initiating a project, through planning, execution, control,', 1, 'Internal', 'Technical'),
('tch019', 'Innovation and Change Management', 'the organization that constantly reinvents itself to be relevant has a better chance of making progress', 1, 'External', 'Technical');

-- --------------------------------------------------------

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
CREATE TABLE `skills` (
  `skill_id` int NOT NULL,
  `skill_name` varchar(64) NOT NULL,
  `skill_category` varchar(64) NOT NULL,
  `skill_desc` varchar(512) NOT NULL,
  `skill_status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `skills`
--

INSERT INTO `skills` (`skill_id`, `skill_name`, `skill_category`, `skill_desc`, `skill_status`) VALUES
(1, 'Creative Thinking', 'Thinking Critically', 'Adopt diverse perspectives in combining ideas or information and making connections between different fields to create different ideas, improvements and solutions', 0),
(2, 'Front-End Engineering and Design', 'Engineering Design Management\r\n', 'Manage Front-End Engineering and Design for equipment, components and systems', 1),
(3, '3D Modelling', 'Engineering Design Management', 'Generate 3D models using a variety of modelling software to represent characteristics of a real-world system', 1),
(4, 'Artificial Intelligence Application', 'Technology Road Mapping', 'Apply algorithmic, statistical and engineering knowledge to integrate artificial intelligence into engineering and maintenance processes', 1),
(5, 'Data and Statistical Analytics', 'Technology Road Mapping', 'Identify data sets for the application of statistical techniques to analyse and interpret large complex data to uncover trends or patterns in order to locate and define new process\r\nimprovement opportunities', 1),
(6, 'Internet of Things (IoT) Management', 'Technology Road Mapping', 'Interrelate computing devices, equipment and machines data in a networked environment to provide specific solutions', 0),
(7, 'Robotic and Automation Technology Application', 'Technology Road Mapping', 'Integrate robotic and automation technologies in engineering services, including construction, operations and maintenance so as to enhance productivity and precision and to reduce\r\nreliance on manual tasks', 1),
(8, 'Workplace Safety and Health Culture Development', 'Workplace Safety and Health (WSH) Management', 'Create and maintain a Workplace Safety and Health culture based on a common set of attitudes, behaviours, and competencies', 1),
(9, 'Financial Analysis', 'Project Finance', 'Analyse the financial statements and data to provide insights about the financial performance and position of the organisation over time', 1),
(10, 'Capital Expenditure and Investment Evaluation', 'Project Finance', 'Assess investments based on alignment with strategies, affordability, acceptable returns and prioritisation of options', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`course_id`);

--
-- Indexes for table `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`skill_id`),
  ADD UNIQUE KEY `skill_name` (`skill_name`);

--
-- Indexes for table `skills_courses`
--
ALTER TABLE `skills_courses`
  ADD PRIMARY KEY (`skill_id`,`course_id`),
  ADD KEY `course_id` (`course_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `skills`
--
ALTER TABLE `skills`
  MODIFY `skill_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `skills_courses`
--
ALTER TABLE `skills_courses`
  ADD CONSTRAINT `skills_courses_ibfk_1` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`skill_id`),
  ADD CONSTRAINT `skills_courses_ibfk_2` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
