CREATE DATABASE IF NOT EXISTS malhaedgh_db DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE malhaedgh_db;

CREATE TABLE `users` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `business_data_id` INT,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `business_data` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `business_type` VARCHAR(255),
  `corporation_type` VARCHAR(255),
  `industry` VARCHAR(255),
  `region_city` VARCHAR(50),
  `region_district` VARCHAR(50),
  `representative_birthday` VARCHAR(10),
  `representative_gender` VARCHAR(10),
  `revenue` FLOAT,
  `employees` INT
);

CREATE TABLE `alerts` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `business_data_id` INT,
  `title` VARCHAR(255),
  `keywords` TEXT,
  `line_summarization` VARCHAR(255),
  `text_summarization` TEXT,
  `task_summarization` TEXT,
  `detail_report` TEXT,
  `due_date` TIMESTAMP
);

CREATE TABLE `user_alert_mapping` (
  `user_id` INT,
  `alert_id` INT,
  `is_read` BOOLEAN,
  PRIMARY KEY (`user_id`, `alert_id`)
);

CREATE INDEX idx_user_id ON user_alert_mapping (user_id);
