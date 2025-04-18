CREATE OR REPLACE FUNCTION import_customer_csv(table_name TEXT, file_path TEXT)
RETURNS VOID AS $$
BEGIN
	EXECUTE format(
		'CREATE TABLE IF NOT EXISTS %I (
			event_time TIMESTAMPTZ NOT NULL,
			event_type TEXT NOT NULL,
			product_id INT NOT NULL,
			price NUMERIC(10,2) NOT NULL,
			user_id BIGINT NOT NULL,
			user_session UUID
		)', table_name
	);

	EXECUTE format(
		'COPY %I FROM %L DELIMITER '','' CSV HEADER', table_name, file_path
	);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION import_all_customer_files(folder_path TEXT)
RETURNS void AS $$
DECLARE
    file_name TEXT;
    table_name TEXT;
BEGIN
    FOR file_name IN SELECT pg_ls_dir(folder_path) LOOP
        IF file_name LIKE '%.csv' THEN
            table_name := regexp_replace(file_name, '\.csv$', '');
            PERFORM import_customer_csv(table_name, folder_path || file_name);
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT import_all_customer_files('/csvfiles/customer/');