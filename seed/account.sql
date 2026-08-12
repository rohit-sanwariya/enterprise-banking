 

INSERT INTO accounts.account (
    id,
    account_number,
    customer_id,
    account_type,
    status,
    currency,
    opened_at,
    created_at,
    updated_at
)
SELECT
    gen_random_uuid(),
    'ACC000000001',
    id,
    'SAVINGS',
    'ACTIVE',
    'INR',
    NOW(),
    NOW(),
    NOW()
FROM customer.customer c
WHERE c.customer_number = 'CUS000001';


INSERT INTO accounts.account (
    id,
    account_number,
    customer_id,
    account_type,
    status,
    currency,
    opened_at,
    created_at,
    updated_at
)
SELECT
    gen_random_uuid(),
    'ACC000000002',
    id,
    'CURRENT',
    'ACTIVE',
    'INR',
    NOW(),
    NOW(),
    NOW()
FROM customer.customer c
WHERE c.customer_number = 'CUS000002';

INSERT INTO accounts.account (
    id,
    account_number,
    customer_id,
    account_type,
    status,
    currency,
    opened_at,
    created_at,
    updated_at
)
SELECT
    gen_random_uuid(),
    'ACC000000003',
    id,
    'SAVINGS',
    'ACTIVE',
    'INR',
    NOW(),
    NOW(),
    NOW()
FROM customer.customer c
WHERE c.customer_number = 'CUS000003';
INSERT INTO accounts.account (
    id,
    account_number,
    customer_id,
    account_type,
    status,
    currency,
    opened_at,
    created_at,
    updated_at
)
SELECT
    gen_random_uuid(),
    'ACC000000004',
    id,
    'CURRENT',
    'ACTIVE',
    'INR',
    NOW(),
    NOW(),
    NOW()
FROM customer.customer c
WHERE c.customer_number = 'CUS000003';