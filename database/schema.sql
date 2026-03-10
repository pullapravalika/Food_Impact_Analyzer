-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100)
);

-- Food logs
CREATE TABLE food_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    food_name VARCHAR(100),
    calories INT,
    category VARCHAR(50),
    health_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Streak tracker
CREATE TABLE streak_tracker (
    user_id INT PRIMARY KEY,
    healthy_streak INT DEFAULT 0,
    junk_streak INT DEFAULT 0
);