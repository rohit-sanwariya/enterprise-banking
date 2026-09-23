package customer

import (
	"fmt"
	"math/rand"
)

func generateCustomerNumber() string {
	number := rand.Intn(999999) + 1

	return fmt.Sprintf("CUS%06d", number)
}
