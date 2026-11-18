-- TEST DATABASE INITIALIZATION SCRIPT

CREATE DATABASE IF NOT EXISTS test_order_management_db;

GRANT ALL PRIVILEGES ON test_order_management_db.*
TO 'app_user'@'%';
