CREATE DATABASE stock_prediction;
    
USE stock_prediction;     
     
CREATE TABLE users_data (            
    user_id VARCHAR(8) PRIMARY KEY,    
    user_name VARCHAR(255) NOT NULL,     
    password VARCHAR(255) NOT NULL,
    city VARCHAR(255),  
    phone_no VARCHAR(20),    
    
    address TEXT
);

CREATE TABLE single_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(8),
    stock_name VARCHAR(50),
    time_period INT,
    predicted_profit FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users_data(user_id)
);

CREATE TABLE recommendation_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(8),
    stock_name VARCHAR(50),
    investment_amount FLOAT,
    time_period INT,
    predicted_profit FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users_data(user_id)
);

