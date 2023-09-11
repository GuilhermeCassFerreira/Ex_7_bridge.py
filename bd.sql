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

-- Inserções de exemplo na tabela 'users' (senhas não criptografadas)
INSERT INTO users (username, email, password, admin) VALUES
    ('admin', 'admin@example.com', 'senha_admin', true),
    ('user1', 'user1@example.com', 'senha_user1', false),
    ('user2', 'user2@example.com', 'senha_user2', false);

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
