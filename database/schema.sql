-- Tạo database
CREATE DATABASE apartment_management;

-- Kết nối đến database
\c apartment_management

-- Tạo bảng Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng Apartments
CREATE TABLE apartments (
    id SERIAL PRIMARY KEY,
    apartment_number VARCHAR(20) UNIQUE NOT NULL,
    floor INTEGER NOT NULL,
    building VARCHAR(50) NOT NULL,
    area FLOAT NOT NULL,
    bedrooms INTEGER NOT NULL,
    bathrooms INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available',
    monthly_rent DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng Residents
CREATE TABLE residents (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20) NOT NULL,
    apartment_id INTEGER REFERENCES apartments(id),
    move_in_date DATE NOT NULL,
    move_out_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng Payments
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    resident_id INTEGER REFERENCES residents(id),
    apartment_id INTEGER REFERENCES apartments(id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_type VARCHAR(20) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo bảng Maintenance
CREATE TABLE maintenance (
    id SERIAL PRIMARY KEY,
    apartment_id INTEGER REFERENCES apartments(id),
    reported_by INTEGER REFERENCES residents(id),
    issue_description TEXT NOT NULL,
    reported_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    resolved_date DATE,
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tạo indexes
CREATE INDEX idx_apartments_status ON apartments(status);
CREATE INDEX idx_residents_apartment_id ON residents(apartment_id);
CREATE INDEX idx_payments_resident_id ON payments(resident_id);
CREATE INDEX idx_payments_apartment_id ON payments(apartment_id);
CREATE INDEX idx_maintenance_apartment_id ON maintenance(apartment_id);
CREATE INDEX idx_maintenance_status ON maintenance(status);
