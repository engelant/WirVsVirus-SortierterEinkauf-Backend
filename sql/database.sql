-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema sichereseinkaufen
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sichereseinkaufen
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sichereseinkaufen` DEFAULT CHARACTER SET utf8 ;
USE `sichereseinkaufen` ;

-- -----------------------------------------------------
-- Table `sichereseinkaufen`.`market_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sichereseinkaufen`.`market_type` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sichereseinkaufen`.`market`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sichereseinkaufen`.`market` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `google_track` VARCHAR(255) NULL DEFAULT NULL,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  `type` INT(11) NOT NULL,
  `ltdtude` DOUBLE(9,6) NOT NULL,
  `lngtude` DOUBLE(9,6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `market_id` (`id` ASC),
  INDEX `position_lat_long` (`ltdtude` ASC, `lngtude` ASC),
  INDEX `position_long_lat` (`lngtude` ASC, `ltdtude` ASC),
  INDEX `fk_market_market_type` (`type` ASC),
  CONSTRAINT `fk_market_market_type`
    FOREIGN KEY (`type`)
    REFERENCES `sichereseinkaufen`.`market_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 33
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sichereseinkaufen`.`market_pax`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sichereseinkaufen`.`market_pax` (
  `market_id` INT(11) NOT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `pax_count` INT(11) NOT NULL,
  `average_presence_time` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`market_id`, `timestamp`),
  INDEX `fk_market_pax_market_idx` (`market_id` ASC),
  CONSTRAINT `fk_market_pax_market`
    FOREIGN KEY (`market_id`)
    REFERENCES `sichereseinkaufen`.`market` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sichereseinkaufen`.`market_stats`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sichereseinkaufen`.`market_stats` (
  `market_id` INT(11) NOT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ranking` SMALLINT(6) NOT NULL,
  PRIMARY KEY (`market_id`, `timestamp`),
  INDEX `fk_market_stats_market1_idx` (`market_id` ASC),
  CONSTRAINT `fk_market_stats_market1`
    FOREIGN KEY (`market_id`)
    REFERENCES `sichereseinkaufen`.`market` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sichereseinkaufen`.`mqtt`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sichereseinkaufen`.`mqtt` (
  `id` SMALLINT(5) UNSIGNED NULL DEFAULT NULL,
  `ts` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `active` TINYINT(4) NOT NULL DEFAULT '1',
  `topic` TEXT NOT NULL,
  `value` LONGTEXT NOT NULL,
  `qos` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0',
  `retain` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0',
  PRIMARY KEY (`topic`(1024)),
  INDEX `id` (`id` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sichereseinkaufen`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sichereseinkaufen`.`products` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 29
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `sichereseinkaufen`.`product_market`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sichereseinkaufen`.`product_market` (
  `market_id` INT(11) NOT NULL,
  `products_id` INT(11) NOT NULL,
  `amount` INT(11) NULL DEFAULT NULL,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`market_id`, `products_id`),
  INDEX `fk_product_market_market_idx` (`market_id` ASC),
  INDEX `fk_product_market_products1_idx` (`products_id` ASC),
  CONSTRAINT `fk_product_market_market`
    FOREIGN KEY (`market_id`)
    REFERENCES `sichereseinkaufen`.`market` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_market_products1`
    FOREIGN KEY (`products_id`)
    REFERENCES `sichereseinkaufen`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
