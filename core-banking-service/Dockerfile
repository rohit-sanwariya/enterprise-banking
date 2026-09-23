FROM golang:1.27-alpine

WORKDIR /app

RUN apk add --no-cache git

RUN go install github.com/air-verse/air@latest
RUN go install github.com/swaggo/swag/cmd/swag@latest
COPY go.mod go.sum ./

RUN go mod download

COPY . .

EXPOSE 8080

CMD ["air"]