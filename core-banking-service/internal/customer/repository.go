package customer

import (
	"context"
	"github.com/jackc/pgx/v5"
)

type CustomerRepository struct {
	db *pgx.Conn
}

func NewCustomerRepository(db *pgx.Conn) *CustomerRepository {
	return &CustomerRepository{
		db: db,
	}
}

func (r *CustomerRepository) Create(ctx context.Context, customer *Customer) error {
	_, err := r.db.Exec(
		ctx,
		insertCustomerQuery,
		customer.ID,
		customer.CustomerNumber,
		customer.CustomerType,
		customer.FirstName,
		customer.MiddleName,
		customer.LastName,
		customer.DateOfBirth,
		customer.Email,
		customer.PhoneNumber,
		customer.Status,
		customer.Trash,
		customer.TrashedAt,
		customer.CreatedAt,
		customer.UpdatedAt,
	)

	return err
}

func (r *CustomerRepository) List(ctx context.Context,page int,limit int) ([]*CustomerListItem, error) {
	offset := (page - 1) * limit
	rows, err := r.db.Query(
		ctx,
		listCustomerQuery,
		limit,
		offset,
	)

	if err != nil {
		return nil, err
	}

	defer rows.Close()

	var customers []*CustomerListItem

	for rows.Next() {
		customer := &CustomerListItem{}

		err := rows.Scan(
			&customer.FirstName,
			&customer.MiddleName,
			&customer.LastName,
			&customer.DateOfBirth,
			&customer.CustomerNumber,
			&customer.CustomerType,
			&customer.Email,
			&customer.PhoneNumber,
			&customer.Status,
		)

		if err != nil {
			return nil, err
		}

		customers = append(customers, customer)
	}

	return customers, err
}
