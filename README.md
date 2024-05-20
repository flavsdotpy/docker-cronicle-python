# docker-cronicle-python

Docker project for Cronicle, bundling a python environment and script runner.

## Instalation

### 1. Prepare working dir

`mkdir $HOME/.cronicle`

### 2. Build the image

`docker build -t cronicle-python .`

_Obs: from this repo root_

### 3. Run container

```shell
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
```

### 4. Access the Cronicle UI and configure the Python plugin

TBD

## Acknowledgments

Thanks `soulteary` for making Cronicle available for Docker.

## Authors

* **[flavsdotpy](github.com/flavsdotpy)**
