CREATE DATABASE IF NOT EXISTS malhaedgh_db;

USE malhaedgh_db;

CREATE TABLE `users` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `username` VARCHAR(20),
  `business_type` VARCHAR(15),
  `corporation_type` VARCHAR(15),
  `industry` VARCHAR(60),
  `region` VARCHAR(40),
  `representative_birthday` VARCHAR(12),
  `representative_gender` VARCHAR(5),
  `revenue` float,
  `employees` int,
  `created_at` timestamp
);

CREATE TABLE `alerts` (
  `id` integer PRIMARY KEY AUTO_INCREMENT,
  `title` VARCHAR(255),
  `keywords` JSON,
  `line_summarization` VARCHAR(255),
  `text_summarization` text,
  `task_summarization` text,
  `detail_report` text
);

CREATE TABLE `user_alert_mapping` (
  `user_id` integer,
  `alert_id` integer
);

CREATE INDEX idx_user_id ON user_alert_mapping (user_id);