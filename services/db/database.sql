-- Database: `ljps`
--
CREATE DATABASE IF NOT EXISTS ljps;
USE ljps;

-- ---------------------------------------------------------------- --
--                     SKILLS TABLE                       --
-- ---------------------------------------------------------------- --
--
-- Table structure for table `SKILLS` --
--
DROP TABLE IF EXISTS skills;

CREATE TABLE IF NOT EXISTS skills (
	skill_id INT NOT NULL auto_increment,
	skill_name varchar(64) NOT NULL UNIQUE,
	skill_category varchar(64) NOT NULL,
    skill_desc varchar(64) NOT NULL,
    skill_status BOOLEAN NOT NULL,
	PRIMARY KEY(skill_id)
) ENGINE=InnoDB;


--
-- Insert Data into SKILLS -- 
--

INSERT INTO skills(skill_name,skill_category,skill_desc,skill_status) 
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

