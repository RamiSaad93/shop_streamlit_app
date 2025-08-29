-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema shop_project
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema shop_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `shop_project` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `shop_project` ;

-- -----------------------------------------------------
-- Table `shop_project`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shop_project`.`customers` (
  `Customer_id` INT NOT NULL AUTO_INCREMENT,
  `Customer_Name` VARCHAR(45) NULL DEFAULT NULL,
  `Email` VARCHAR(100) NULL DEFAULT NULL,
  `Password` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`Customer_id`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `shop_project`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shop_project`.`orders` (
  `Order_id` INT NOT NULL AUTO_INCREMENT,
  `Order_Date` DATE NULL DEFAULT NULL,
  `Customer_id` INT NOT NULL,
  PRIMARY KEY (`Order_id`),
  INDEX `fk_Orders_Costomers1_idx` (`Customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_Orders_Costomers1`
    FOREIGN KEY (`Customer_id`)
    REFERENCES `shop_project`.`customers` (`Customer_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `shop_project`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shop_project`.`products` (
  `Product_id` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(100) NOT NULL,
  `Price` DECIMAL(10,2) NULL DEFAULT NULL,
  `Stock` INT NULL DEFAULT NULL,
  PRIMARY KEY (`Product_id`),
  UNIQUE INDEX `Product_id_UNIQUE` (`Product_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `shop_project`.`order_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `shop_project`.`order_items` (
  `Order_Item_id` INT NOT NULL AUTO_INCREMENT,
  `Product_id` INT NOT NULL,
  `Order_id` INT NOT NULL,
  `Quantity` INT NOT NULL,
  `Price` DECIMAL(6,2) NULL DEFAULT NULL,
  PRIMARY KEY (`Order_Item_id`),
  INDEX `fk_Products_has_Orders_Orders1_idx` (`Order_id` ASC) VISIBLE,
  INDEX `fk_Products_has_Orders_Products1_idx` (`Product_id` ASC) VISIBLE,
  CONSTRAINT `fk_Products_has_Orders_Orders1`
    FOREIGN KEY (`Order_id`)
    REFERENCES `shop_project`.`orders` (`Order_id`),
  CONSTRAINT `fk_Products_has_Orders_Products1`
    FOREIGN KEY (`Product_id`)
    REFERENCES `shop_project`.`products` (`Product_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
