package email

import (
	"fmt"
	"net/smtp"
)

type Sender struct {
	host string
	port string
	from string
}

func NewSender(host, port, from string) *Sender {
	return &Sender{
		host: host,
		port: port,
		from: from,
	}
}

func (s *Sender) Send(to, subject, body string) error {
	address := fmt.Sprintf("%s:%s", s.host, s.port)

	message := []byte(
		"From: " + s.from + "\r\n" +
			"To: " + to + "\r\n" +
			"Subject: " + subject + "\r\n" +
			"\r\n" +
			body,
	)

	return smtp.SendMail(
		address,
		nil,
		s.from,
		[]string{to},
		message,
	)
}