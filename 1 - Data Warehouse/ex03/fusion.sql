ALTER TABLE customers
ADD COLUMN category_id BIGINT,
ADD COLUMN category_code TEXT,
ADD COLUMN brand TEXT;

UPDATE customers c
	SET 
		category_id = i.category_id,
		category_code = i.category_code,
		brand = i.brand
	FROM items i
	WHERE c.product_id = i.product_id;