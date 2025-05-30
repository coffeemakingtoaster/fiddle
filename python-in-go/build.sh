docker build -t python-in-go:latest . && docker run --rm -v ./test.yaml:/app/test.yaml python-in-go:latest
