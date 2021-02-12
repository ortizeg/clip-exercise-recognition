gcr_location = deep-ego
model_name ?= clip-exercise-recognizer
api_version ?= latest
api_tag ?= gcr.io/${gcr_location}/${model_name}-api
dev_tag ?= gcr.io/${gcr_location}/${model_name}-dev
model_version ?= $(shell cat .model_version)

build-dev:
	echo 'Building dev container.'
	docker build \
		-t $(dev_tag):$(api_version) \
		-t $(dev_tag):latest \
		-f Dockerfile.dev .

dev: build-dev
	echo 'Starting dev container in interactive shell mode.'
	docker run \
		--name dev \
		--net=host \
		-it \
		-d \
		--gpus all \
		--rm \
		-v `pwd`:/workspace \
		$(dev_tag):$(api_version) \
		jupyter lab --ip=0.0.0.0 --ServerApp.token='development' --ServerApp.password='development' --allow-root --no-browser

dev-cpu: build-dev
	echo 'Starting dev container in interactive shell mode.'
	docker run \
		--name dev \
		--net=host \
		-it \
		-d \
		--rm \
		-v `pwd`:/workspace \
		$(dev_tag):$(api_version) \
		jupyter lab --ip=0.0.0.0 --ServerApp.token='development' --ServerApp.password='development' --allow-root --no-browser

triton:
	echo 'Starting Triton model server.'
	docker run \
		--name triton \
		--gpus all \
		--rm -p8000:8000 -p8001:8001 -p8002:8002 \
		-v `pwd`/models/onnx:/models \
		nvcr.io/nvidia/tritonserver:20.10-py3 \
		tritonserver --model-repository=/models
