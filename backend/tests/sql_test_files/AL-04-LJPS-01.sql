DROP TABLE IF EXISTS `learning_journeys`;

DROP TABLE IF EXISTS `learning_journeys`;
CREATE TABLE `learning_journeys` (
  `learning_journey_id` int NOT NULL,
  `learning_journey_name` varchar(50) NOT NULL,
  `staff_id` int NOT NULL,
  `role_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `learning_journeys` (`learning_journey_id`, `learning_journey_name`, `staff_id`, `role_id`) VALUES
(1, 'My LJ to become CEO', 140078, 2),
(2, 'My LJ to become Designer', 140078, 1);