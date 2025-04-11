SET NAMES utf8mb4;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Honeysuckle@123!';
CREATE DATABASE honeysuckle_db CHARACTER SET utf8mb4;
-- CREATE DATABASE scanner_db CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER 'honeysuckle'@'%' IDENTIFIED WITH mysql_native_password BY 'bjuxSNvmq7kWra5b';
GRANT ALL PRIVILEGES ON honeysuckle.* TO 'honeysuckle'@'%';