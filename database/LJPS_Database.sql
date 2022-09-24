-- Database: `LJPS`
--
CREATE DATABASE IF NOT EXISTS LJPS;
USE LJPS;

-- ---------------------------------------------------------------- --
--                     SKILLS TABLE                       --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `SKILLS_SEQ`
--
DROP TABLE IF EXISTS SKILLS_SEQ;

CREATE TABLE SKILLS_SEQ
(
	SKILL_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `SKILLS` --
--
DROP TABLE IF EXISTS SKILLS;

CREATE TABLE IF NOT EXISTS SKILLS (
	SKILL_ID varchar(64) NOT NULL,
	SKILL_NAME varchar(64) NOT NULL UNIQUE,
	SKILL_CATEGORY varchar(64) NOT NULL,
    SKILL_DESC varchar(64) NOT NULL,
    SKILL_STATUS BOOLEAN NOT NULL,
	PRIMARY KEY(SKILL_ID)
) ENGINE=InnoDB;

--
-- Trigger for autoincrement for `SKILLS`
--

DELIMITER $$
CREATE TRIGGER tg_skill_insert
BEFORE INSERT ON SKILLS
FOR EACH ROW
BEGIN
	INSERT INTO SKILLS_SEQ VALUES (NULL);
	SET NEW.SKILL_ID = CONCAT('S', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

--
-- Insert Data into SKILLS -- 
--

INSERT INTO SKILLS(SKILL_NAME,SKILL_CATEGORY,SKILL_DESC,SKILL_STATUS) 
VALUES ('Programming','Development','Pick up new programming skills like Python',TRUE),
	   ('UI/UX','Development','Pick up new UI/UX Design Skills',TRUE);
-- ---------------------------------------------------------------- --
--                     ROLES TABLE                       --
-- ---------------------------------------------------------------- --

--
-- Table structure for table `ROLES_SEQ`
--
DROP TABLE IF EXISTS ROLES_SEQ;

CREATE TABLE ROLES_SEQ
(
	ROLE_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY
);

--
-- Table structure for table `ROLES` --
--
DROP TABLE IF EXISTS ROLES;

CREATE TABLE IF NOT EXISTS ROLES (
	ROLE_ID varchar(64) NOT NULL,
	ROLE_NAME varchar(64) NOT NULL UNIQUE,
	ROLE_DESC varchar(64) NOT NULL,
    ROLE_STATUS boolean NOT NULL,
	PRIMARY KEY(ROLE_ID)
) ENGINE=InnoDB;

--
-- Trigger for autoincrement for `ROLES`
--

DELIMITER $$
CREATE TRIGGER tg_role_insert
BEFORE INSERT ON ROLES
FOR EACH ROW
BEGIN
	INSERT INTO ROLES_SEQ VALUES (NULL);
	SET NEW.ROLE_ID = CONCAT('R', LPAD(LAST_INSERT_ID(), 3, '0'));
END$$
DELIMITER ;

--
-- Insert Data into ROLES -- 
--

INSERT INTO ROLES(ROLE_NAME,ROLE_DESC,ROLE_STATUS) 
VALUES ('Software Developer','Build Web Applications for company',TRUE),
	   ('UX Designer','Design UX for Web Applications',TRUE);

