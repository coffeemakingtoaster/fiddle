lib: ./lib/library.so

./lib/library.so: ./lib/lib.go
	go build -buildmode=c-shared -o ./lib/library.so ./lib/lib.go

exec: ./main

./main: main.go
	go build main.go

all: lib exec

clean:
	rm ./main && rm ./lib/*.{so,h}
