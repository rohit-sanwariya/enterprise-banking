package auth

const createIdentityQuery = `
	INSERT INTO identities (
		id,
		email,
		password_hash,
		customer_id
	)
	VALUES (
		@id,
		@email,
		@password_hash,
		@customer_id
	)
	RETURNING id, email, password_hash, customer_id
`
const getIdentityByEmail = `
	SELECT 
		id,
		customer_id,
		email,
		password_hash
	FROM identities
	WHERE LOWER(email) = LOWER(@email)
	`
