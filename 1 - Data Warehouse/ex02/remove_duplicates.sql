
-- Exact same data
CREATE TEMPORARY TABLE tmp_customers AS
	SELECT DISTINCT * FROM customers;
TRUNCATE customers;
INSERT INTO customers SELECT * FROM tmp_customers;

-- Exact same data but with a event_time difference of 1 second or less
WITH ordered_events AS (
	SELECT ctid, *, LAG(event_time)
		OVER
			(PARTITION BY event_type, product_id, price, user_id, user_session
			ORDER BY event_time)
		AS prev_time
	FROM customers
), duplicates AS (
	SELECT ctid
		FROM ordered_events
		WHERE prev_time IS NOT NULL
			AND EXTRACT(EPOCH FROM (event_time - prev_time)) < 1
)
DELETE FROM customers WHERE ctid IN (SELECT ctid FROM duplicates);