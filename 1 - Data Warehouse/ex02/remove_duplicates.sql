
--Exact same data
DELETE FROM customers t1 USING (
	SELECT MAX(ctid) as keep_ctid, *
	FROM customers
	GROUP BY event_time, event_type, product_id, price, user_id, user_session
	HAVING COUNT(*) > 1
) t2
	WHERE t1.event_time = t2.event_time
		AND t1.event_type = t2.event_type
		AND t1.product_id = t2.product_id
		AND t1.price = t2.price
		AND t1.user_id = t2.user_id
		AND t1.user_session = t2.user_session
		AND t1.ctid <> t2.keep_ctid;

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