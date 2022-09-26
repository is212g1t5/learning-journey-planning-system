-- Database: `LJPS`
--
CREATE DATABASE IF NOT EXISTS LJPS;
USE LJPS;

-- ---------------------------------------------------------------- --
--                     SKILLS TABLE                       --
-- ---------------------------------------------------------------- --
--
-- Table structure for table `SKILLS` --
--
DROP TABLE IF EXISTS SKILLS;

CREATE TABLE IF NOT EXISTS SKILLS (
	SKILL_ID INT NOT NULL auto_increment,
	SKILL_NAME varchar(64) NOT NULL UNIQUE,
	SKILL_CATEGORY varchar(64) NOT NULL,
    SKILL_DESC varchar(64) NOT NULL,
    SKILL_STATUS BOOLEAN NOT NULL,
	PRIMARY KEY(SKILL_ID)
) ENGINE=InnoDB;


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
-- Table structure for table `ROLES` --
--
DROP TABLE IF EXISTS ROLES;

CREATE TABLE IF NOT EXISTS ROLES (
	ROLE_ID int NOT NULL auto_increment,
	ROLE_NAME varchar(64) NOT NULL UNIQUE,
	ROLE_DESC varchar(64) NOT NULL,
    ROLE_STATUS boolean NOT NULL,
	PRIMARY KEY(ROLE_ID)
) ENGINE=InnoDB;


-- Insert Data into ROLES -- 
--

INSERT INTO ROLES(ROLE_NAME,ROLE_DESC,ROLE_STATUS) 
VALUES ('Software Developer','Build Web Applications for company',TRUE),
	   ('UX Designer','Design UX for Web Applications',TRUE);

