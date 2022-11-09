--
-- Table structure for table `courses`
--
DROP TABLE IF EXISTS `skills_roles`;
DROP TABLE IF EXISTS `lj_role_skill`;
DROP TABLE IF EXISTS `lj_courses`;
DROP TABLE IF EXISTS `learning_journeys`;
DROP TABLE IF EXISTS `registration`;
DROP TABLE IF EXISTS `skills_courses`;
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
('COR002', 'Lean Six Sigma Green Belt Certification', 'Apply Lean Six Sigma methodology and statistical tools such as Minitab to be used in process analytics', 1, 'Internal', 'Core');

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
CREATE TABLE `registration` (
  `reg_id` int NOT NULL,
  `course_id` varchar(20) NOT NULL,
  `staff_id` int NOT NULL,
  `reg_status` varchar(11) NOT NULL,
  `completion_status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`reg_id`, `course_id`, `staff_id`, `reg_status`, `completion_status`) VALUES
(1, 'COR001', 140078, 'Registered', 'Completed'),
(2, 'COR002', 140878, 'Registered', 'Completed');
-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
  `role_id` int NOT NULL,
  `role_name` varchar(64) NOT NULL,
  `role_desc` varchar(512) NOT NULL,
  `role_status` tinyint(1) NOT NULL,
  `role_sector` varchar(64) NOT NULL,
  `role_track` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`, `role_desc`, `role_status`, `role_sector`, `role_track`) VALUES
(1, 'Designer', 'The Designer (Engineering Design) develops technical drawings and models based on pre-defined specifications and engineering calculations. He/She interprets engineering calculations and uses design software and modelling methods for preparation of drawings and designs. He identifies relevant design data and highlights design issues where applicable. He also complies with Design for Safety (DfS) regulations and ensures compliance with industry standards and international conventions. He possesses high detail', 1, 'Engineering Services', 'Engineering Design');

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
(2, 'Front-End Engineering and Design', 'Engineering Design Management\r\n', 'Manage Front-End Engineering and Design for equipment, components and systems', 1);
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
(2, 'COR001'),
(2, 'COR002');
-- --------------------------------------------------------

--
-- Table structure for table `skills_roles`
--

DROP TABLE IF EXISTS `skills_roles`;
CREATE TABLE `skills_roles` (
  `skill_id` int NOT NULL,
  `role_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `skills_roles`
--

INSERT INTO `skills_roles` (`skill_id`, `role_id`) VALUES
(1, 1),
(2, 1);
-- --------------------------------------------------------

--
-- Table structure for table `staffs`
--

DROP TABLE IF EXISTS `staffs`;
CREATE TABLE `staffs` (
  `staff_id` int NOT NULL,
  `staff_fname` varchar(50) NOT NULL,
  `staff_lname` varchar(50) NOT NULL,
  `dept` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `group` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `staffs`
--

INSERT INTO `staffs` (`staff_id`, `staff_fname`, `staff_lname`, `dept`, `email`, `group`) VALUES
(140078, 'Amelia', 'Ong', 'Sales', 'Amelia.Ong@allinone.com.sg', 1);
--
-- Indexes for dumped tables
--