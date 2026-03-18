CREATE TABLE ei (
    ei_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    role_id INTEGER,
	FOREIGN KEY (role_id) REFERENCES roles(role_id)
);

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    inn VARCHAR(12),
    address TEXT,
    phone VARCHAR(20),
    is_salesman BOOLEAN,
    is_buyer BOOLEAN
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ei_id INTEGER,
	price NUMERIC(10, 2) NOT NULL,
	FOREIGN KEY (ei_id) REFERENCES ei(ei_id)
);

CREATE TABLE specifications (
    specification_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    product_id INTEGER NOT NULL,
    quantity NUMERIC(10, 3),
	FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

CREATE TABLE specification_materials (
    spec_material_id SERIAL PRIMARY KEY,
    specification_id INTEGER,
    material_id INTEGER,
    quantity NUMERIC(10, 3) NOT NULL,
	FOREIGN KEY (specification_id) REFERENCES specifications(specification_id) ON DELETE CASCADE,
	FOREIGN KEY (material_id) REFERENCES products(product_id)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(20),
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,
	FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_products (
    order_product_id SERIAL PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity NUMERIC(10, 3) NOT NULL,
	FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
	FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE productions (
    production_id SERIAL PRIMARY KEY,
    production_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE production_specifications (
    prod_spec_id SERIAL PRIMARY KEY,
    production_id INTEGER,
    specification_id INTEGER,
    quantity NUMERIC(10, 3) NOT NULL,
	FOREIGN KEY (production_id) REFERENCES productions(production_id) ON DELETE CASCADE,
	FOREIGN KEY (specification_id) REFERENCES specifications(specification_id)
);