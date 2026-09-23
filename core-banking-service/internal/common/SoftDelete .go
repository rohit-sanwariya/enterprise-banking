package common


import (
	"time"
)

type SoftDelete  struct {
	Trash     bool
	TrashedAt *time.Time
}