CREATE TABLE IF NOT EXISTS data_2022_oct (
	event_time TIMESTAMPTZ NOT NULL,
	event_type TEXT NOT NULL,
	product_id INT NOT NULL,
	price NUMERIC(10,2) NOT NULL,
	user_id BIGINT NOT NULL,
	user_session UUID
);

COPY data_2022_oct FROM '/csvfiles/customer/data_2022_oct.csv' DELIMITER ',' CSV HEADER;