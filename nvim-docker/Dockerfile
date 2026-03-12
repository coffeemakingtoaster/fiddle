from alpine:latest

RUN apk add --update-cache \
    fzf \
    neovim \
    git \
    go \
  && rm -rf /var/cache/apk/*

RUN addgroup -S coffee && adduser -h /home/coffee -S coffee -G coffee

USER coffee

RUN git clone --quiet https://github.com/coffeemakingtoaster/kickstart.nvim.git /home/coffee/.config/nvim && \ 
	nvim --headless "+Lazy! sync" +qa

RUN mkdir /home/coffee/code

WORKDIR /home/coffee/code

ENTRYPOINT ["nvim"]

