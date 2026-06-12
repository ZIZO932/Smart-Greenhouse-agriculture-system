-- ==============================================================================
-- VERDEX - Database Schema for XAMPP / phpMyAdmin
-- ==============================================================================
-- Instructions:
-- 1. Open phpMyAdmin in your browser (usually http://localhost/phpmyadmin)
-- 2. Create a new database named: vervex_database
-- 3. Select the `vervex_database` database.
-- 4. Go to the "SQL" tab.
-- 5. Copy and paste the entire code below, then click "Go" to create the table.
-- ==============================================================================

CREATE TABLE IF NOT EXISTS `sensor_data` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `device_id` VARCHAR(20) NOT NULL,
  `temperature` FLOAT NOT NULL,
  `light` FLOAT NOT NULL,
  `moisture` INT(11) NOT NULL,
  `npk_n` FLOAT NOT NULL,
  `npk_p` FLOAT NOT NULL,
  `npk_k` FLOAT NOT NULL,
  `rssi` INT(11) NOT NULL,
  `power` FLOAT DEFAULT 0,
  `deviation` FLOAT DEFAULT 0,
  `event` VARCHAR(50) DEFAULT 'normal',
  `sim_timestamp` VARCHAR(30) DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `setpoints` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `plant` VARCHAR(20) NOT NULL UNIQUE,
  `temp_target` FLOAT NOT NULL,
  `moisture_target` INT(11) NOT NULL,
  `light_on` FLOAT NOT NULL,
  `light_off` FLOAT NOT NULL,
  `n_target` FLOAT DEFAULT 110.0,
  `p_target` FLOAT DEFAULT 22.0,
  `k_target` FLOAT DEFAULT 200.0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `setpoints` (`plant`, `temp_target`, `moisture_target`, `light_on`, `light_off`, `n_target`, `p_target`, `k_target`) 
VALUES 
('basil', 25.0, 60, 4000.0, 8000.0, 110.0, 22.0, 200.0),
('stevia', 25.0, 55, 6000.0, 20000.0, 110.0, 22.0, 200.0)
ON DUPLICATE KEY UPDATE plant=plant;

-- ==============================================================================
-- If the table already exists and you need to ADD the new columns:
-- ==============================================================================
-- ALTER TABLE `sensor_data`
--   ADD COLUMN `power` FLOAT DEFAULT 0 AFTER `rssi`,
--   ADD COLUMN `deviation` FLOAT DEFAULT 0 AFTER `power`,
--   ADD COLUMN `event` VARCHAR(50) DEFAULT 'normal' AFTER `deviation`,
--   ADD COLUMN `sim_timestamp` VARCHAR(30) DEFAULT NULL AFTER `event`;
-- ==============================================================================
