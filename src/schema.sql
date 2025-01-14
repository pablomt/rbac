CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL, -- Cognito User ID
    name VARCHAR(255) NOT NULL,
    first_last_name VARCHAR(255) NOT NULL,
    second_last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID REFERENCES users(id)
);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID REFERENCES users(id)
);

CREATE TABLE user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    role_id UUID REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID REFERENCES users(id)
);

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    resource VARCHAR(100) NOT NULL, -- (example "delta_table", "bucket_1", etc)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID REFERENCES users(id)
);


CREATE TABLE role_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID REFERENCES roles(id),
    permission_id UUID REFERENCES permissions(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID REFERENCES users(id),
    UNIQUE(role_id, permission_id)
);


CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action_type VARCHAR(50) NOT NULL,        -- Acción: 'READ', 'WRITE', 'DELETE'
    resource VARCHAR(255) NOT NULL,          -- Recurso (ej.: 'S3://my-bucket/delta-table')
    granted BOOLEAN NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by UUID REFERENCES users(id)
);


/*
    INSERTS
    INSERT INTO users VALUES ('a659f134-7589-4616-bef1-74b96721295d', 'pablomorenotepichin', 'Pablo', 'Moreno', 'Tepichin', 'pmoretepi@gmail.com', 1, '2025-01-13 01:17:02.62471', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-13 01:17:02.62471', 'a659f134-7589-4616-bef1-74b96721295d');
    INSERT INTO users VALUES ('df1435ca-4849-459f-9ca2-4da4c6ff7452', 'analista1', 'Analista', 'appellido', 'appellido 2', 'analista1@yopmail.com', 2, '2025-01-14 00:01:36.848462', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-14 00:01:36.848462', NULL);

    INSERT INTO roles VALUES ('d3aa3898-94e0-4f73-8224-486f6da269d4', 'super_admin', 'Todos los privilegios', '2025-01-13 01:22:24.35443', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-13 01:22:24.35443', NULL);
    INSERT INTO roles VALUES ('5113b585-5f31-4d26-a3fe-c8a6f3889a3d', 'analista_role', 'Permisos de lectura en delta table 2', '2025-01-14 00:03:02.780137', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-14 00:03:02.780137', NULL);

    INSERT INTO user_roles VALUES ('85a03552-7dfe-4e96-85a4-386a7f41723f', 'a659f134-7589-4616-bef1-74b96721295d', 'd3aa3898-94e0-4f73-8224-486f6da269d4', '2025-01-13 01:23:52.769344', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-13 01:23:52.769344', NULL);
    INSERT INTO user_roles VALUES ('27b79c76-fa23-4d50-bbe0-037ad5da164c', 'df1435ca-4849-459f-9ca2-4da4c6ff7452', '5113b585-5f31-4d26-a3fe-c8a6f3889a3d', '2025-01-14 00:08:28.988783', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-14 00:08:28.988783', NULL);

    INSERT INTO permissions VALUES ('df9dd89a-9a31-4552-a3a0-bec52a1caa89', 'read', 'lectura', 'delta_table', '2025-01-13 01:24:38.139399', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-13 01:24:38.139399', NULL);
    INSERT INTO permissions VALUES ('b015a695-50e0-4443-8a92-406b448c925b', 'read', 'lectura', 'delta_table_2', '2025-01-14 00:05:43.610455', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-14 00:05:43.610455', NULL);

    INSERT INTO role_permissions VALUES ('1d644bef-ac51-41bf-b9f3-65d067c83bf0', 'd3aa3898-94e0-4f73-8224-486f6da269d4', 'df9dd89a-9a31-4552-a3a0-bec52a1caa89', '2025-01-13 01:25:49.887188', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-13 01:25:49.887188', NULL);
    INSERT INTO role_permissions VALUES ('9cc03a59-8952-4415-9ca5-fe069e424770', '5113b585-5f31-4d26-a3fe-c8a6f3889a3d', 'b015a695-50e0-4443-8a92-406b448c925b', '2025-01-14 00:46:28.590821', 'a659f134-7589-4616-bef1-74b96721295d', '2025-01-14 00:46:28.590821', NULL);

    select u.email, u.name, r.name, p.name, p.description, p.resource from users u
    join user_roles ur on u.id = ur.user_id
    join roles r on ur.role_id = r.id
    left join role_permissions rp on r.id = rp.role_id
    left join permissions p on rp.permission_id = p.id;
*/