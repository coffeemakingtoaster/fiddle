FROM golang:latest

WORKDIR /app

COPY . .

RUN go build -o sender

ENTRYPOINT ["/app/sender"]
