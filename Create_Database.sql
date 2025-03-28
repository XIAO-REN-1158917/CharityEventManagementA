-- CREATE SCHEMA IF NOT EXISTS `vote` DEFAULT CHARACTER SET utf8 ;
-- USE `vote` ;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `competition_themes`;
CREATE TABLE `competition_themes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,  
  `application_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `theme_applications`;
CREATE TABLE `theme_applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `theme_name` varchar(50) NOT NULL,
  `theme_description` varchar(255) NOT NULL,
  `applicant_id` int NOT NULL,
  `applicant` varchar(20) NOT NULL,
  `applying_time` timestamp NOT NULL,  
  `status` enum('pending','approved','rejected') NOT NULL,  
  `rejection_reason` varchar(255) DEFAULT NULL,
  `operator_id` int DEFAULT NULL,
  `operator` varchar(20) DEFAULT NULL,
  `operation_time` timestamp DEFAULT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `user_theme_role`;
CREATE TABLE `user_theme_role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `theme_id` int NOT NULL,
  `user_id` int NOT NULL,
  `role` enum('scrutineer','admin') NOT NULL,    
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `banned_voters`;
CREATE TABLE `banned_voters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `theme_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `competitions`;
CREATE TABLE `competitions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `voting_start_date` date NOT NULL,
  `voting_end_date` date NOT NULL,
  `status` enum('pending','ongoing','ended','published') NOT NULL,
  `theme_id` int NOT NULL,
  `theme_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `competitors`;
CREATE TABLE `competitors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,
  `image` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ;

DROP TABLE IF EXISTS `competition_competitors`;
CREATE TABLE `competition_competitors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `competition_id` int NOT NULL,
  `competitor_id` int NOT NULL,
  `vote_count` int DEFAULT NULL,
  `vote_ratio` DECIMAL(4,3) DEFAULT NULL,
  `is_winner` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `competition_competitors_competitions` (`competition_id`),
  CONSTRAINT `competition_competitors_competitions` FOREIGN KEY (`competition_id`) REFERENCES `competitions` (`id`)
);

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password_hash` varchar(64) NOT NULL,
  `email` varchar(255) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `avatar` varchar(64) NOT NULL,
  `role` enum('voter','scrutineer','admin') NOT NULL,
  `status` enum('active','inactive') NOT NULL,
  `voting_permission` enum('allowed','banned') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UK` (`username`),
  UNIQUE KEY `email_UK` (`email`)
);

DROP TABLE IF EXISTS `votes`;
CREATE TABLE `votes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `competition_competitor_id` int NOT NULL,
  `voter_id` int NOT NULL,
  `voting_time` timestamp NOT NULL,
  `voting_ip` varchar(50) NOT NULL,
  `status` enum('valid','invalid') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `votes_users` (`voter_id`),
  CONSTRAINT `votes_users` FOREIGN KEY (`voter_id`) REFERENCES `users` (`id`)
);

DROP TABLE IF EXISTS `announcements`;

SET FOREIGN_KEY_CHECKS = 1;