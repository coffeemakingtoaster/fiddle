FROM golang:1.24.3-bookworm AS build

WORKDIR /build

COPY . .

RUN make all

FROM python:3.13 AS runtime

WORKDIR /app

COPY --from=build /build/main .
COPY --from=build /build/lib/*.h /build/lib/*.so /build/lib/*.py ./lib/

CMD ["./main"]
