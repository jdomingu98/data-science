SELECT event_type AS element, COUNT(*) AS recording
	FROM customers
	GROUP BY event_type;