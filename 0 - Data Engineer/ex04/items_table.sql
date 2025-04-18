CREATE TABLE IF NOT EXISTS items (
	product_id INT NOT NULL,
	category_id BIGINT,
	category_code TEXT,
	brand TEXT
);

COPY items FROM '/csvfiles/item/item.csv' DELIMITER ',' CSV HEADER;