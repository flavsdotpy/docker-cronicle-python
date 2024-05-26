

prepare:
	mkdir $HOME/.cronicle

build:
	docker build -t cronicle-python .

run:
	docker run \
		-v /etc/localtime:/etc/localtime:ro \
		-v /etc/timezone:/etc/timezone:ro \
		-v $HOME/.cronicle/data:/opt/cronicle/data:rw \
		-v $HOME/.cronicle/logs:/opt/cronicle/logs:rw \
		-v $HOME/.cronicle/plugins:/opt/cronicle/plugins:rw \
		-v $HOME/.cronicle/scripts:/opt/cronicle/scripts:rw \
		-p 3012:3012 \
		-d \
		--restart always \
		--name cronicle \
		cronicle-python
