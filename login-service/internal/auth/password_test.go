package auth

import "testing"

func TestHashPassword(t *testing.T) {
	password := "secret123"

	hash, err := HashPassword(password)
	if err != nil {
		t.Fatalf("HashPassword() error = %v", err)
	}

	if hash == password {
		t.Fatal("password must not be stored as plaintext")
	}

	if hash == "" {
		t.Fatal("password hash must not be empty")
	}
}

func TestVerifyPassword(t *testing.T) {
	password := "secret123"

	hash, err := HashPassword(password)
	if err != nil {
		t.Fatalf("HashPassword() error = %v", err)
	}

	valid, err := VerifyPassword(password, hash)
	if err != nil {
		t.Fatalf("VerifyPassword() error = %v", err)
	}

	if !valid {
		t.Fatal("expected password to be valid")
	}
}

func TestVerifyPasswordWrongPassword(t *testing.T) {
	password := "secret123"

	hash, err := HashPassword(password)
	if err != nil {
		t.Fatalf("HashPassword() error = %v", err)
	}

	valid, err := VerifyPassword("wrong-password", hash)
	if err != nil {
		t.Fatalf("VerifyPassword() error = %v", err)
	}

	if valid {
		t.Fatal("expected wrong password to be rejected")
	}
}

func TestHashPasswordUsesDifferentSalt(t *testing.T) {
	password := "secret123"

	hash1, err := HashPassword(password)
	if err != nil {
		t.Fatalf("HashPassword() error = %v", err)
	}

	hash2, err := HashPassword(password)
	if err != nil {
		t.Fatalf("HashPassword() error = %v", err)
	}

	if hash1 == hash2 {
		t.Fatal("same password should produce different hashes because of random salts")
	}
}
