FROM golang:latest

WORKDIR /app

COPY . .

RUN go build -o receiver

ENTRYPOINT ["/app/receiver"]
