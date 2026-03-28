CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Администратор', 'Пользователь')),
    is_blocked BOOLEAN DEFAULT FALSE,
    failed_attempts INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, role) VALUES 
('admin', 'admin123', 'Администратор'),
('user1', 'user123', 'Пользователь');

ALTER TABLE users ADD COLUMN employee_id INTEGER REFERENCES employees(employee_id);


INSERT INTO roles (name) VALUES
('Менеджер по продажам'),
('Технолог'),
('Начальник производства'),
('Экономист'),
('Кладовщик');

ALTER TABLE users ADD COLUMN role_id INTEGER REFERENCES roles(role_id);

UPDATE users SET role_id = 1 WHERE role = 'Администратор';
UPDATE users SET role_id = 2 WHERE role = 'Пользователь';