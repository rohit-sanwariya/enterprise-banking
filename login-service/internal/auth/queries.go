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
