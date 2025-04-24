CREATE TABLE IF NOT EXISTS customers (
	event_time TIMESTAMPTZ NOT NULL,
	event_type TEXT NOT NULL,
	product_id BIGINT NOT NULL,
	price NUMERIC(10,2) NOT NULL,
	user_id BIGINT NOT NULL,
	user_session UUID
);

DO $$
DECLARE
    tab text;
BEGIN
    FOR tab IN 
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public' AND tablename LIKE 'data\_202_\_%' ESCAPE '\'
    LOOP
        EXECUTE format('
            INSERT INTO customers
            SELECT * FROM %I
        ', tab);
    END LOOP;
END $$;