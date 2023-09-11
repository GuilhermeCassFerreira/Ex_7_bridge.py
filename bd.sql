-- Criação do banco de dados PostgreSQL (caso não exista)
CREATE DATABASE postgres;

-- Conexão ao banco de dados
\c postgres;

-- Criação da tabela 'users'
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    admin BOOLEAN DEFAULT false,
    auth_token VARCHAR(255)
);

-- Inserções de exemplo na tabela 'users' 
INSERT INTO users (username, email, password, admin) VALUES
    ('admin', 'admin@example.com', '$2b$12$RCM7h7cpaO.oWYQc.GIwL.q/yT.XC3PZU1WIr6OwRhPvff6jAKJHW', true), --senha: senha_admin
    ('user1', 'user1@example.com', '$2b$12$R0y27WksjhxWHR.1.6t8AunQFgVYh.WaG0.OleX4bjxTgfv5f2gkK', false), --senha: senha_user1
    ('user2', 'user2@example.com', '$2b$12$rWlUxy9OYMyhnRi9FvS8bO/QUSjg2j8oHfYf5XT8P95BwHTv0Fyaa', false); --senha: senha_user2

-- Criação da tabela 'tasks'
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN
);

-- Inserções de exemplo na tabela 'tasks'
INSERT INTO tasks (title, completed) VALUES
    ('Fazer compras', false),
    ('Estudar para a prova', true);
