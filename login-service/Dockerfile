FROM golang:1.27-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o login-service ./cmd/server


FROM alpine:3.22

WORKDIR /app

COPY --from=builder /app/login-service .

EXPOSE 8080

CMD ["./login-service"]