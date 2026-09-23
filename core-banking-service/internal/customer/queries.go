package customer

const insertCustomerQuery = `
	INSERT INTO customer.customer (
		id,
		customer_number,
		customer_type,
		first_name,
		middle_name,
		last_name,
		date_of_birth,
		email,
		phone_number,
		status,
		trash,
		trashed_at,
		created_at,
		updated_at
	)
	VALUES (
		$1, $2, $3, $4, $5, $6, $7,
		$8, $9, $10, $11, $12, $13, $14
	)
`
const deleteCustomerQuery = `
    UPDATE customer.customer
    SET trash = true,
        trashed_at = NOW()
    WHERE customer_number = $1;
`
const listCustomerQuery = `
        SELECT 
            first_name,
            middle_name,
            last_name,
            date_of_birth,
            customer_number,
            customer_type,
            email,
            phone_number,
            status 
        FROM customer.customer 
        WHERE trash = false
		LIMIT $1
		OFFSET $2
		;
    `
