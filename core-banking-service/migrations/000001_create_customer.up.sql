CREATE SCHEMA IF NOT EXISTS customer;

CREATE TABLE IF NOT EXISTS customer.customer (
    id UUID PRIMARY KEY,
    customer_number VARCHAR(20) NOT NULL UNIQUE,
    customer_type VARCHAR(20) NOT NULL DEFAULT 'INDIVIDUAL',
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL,
    trash BOOLEAN NOT NULL DEFAULT FALSE,
    trashed_at TIMESTAMPTZ
);
