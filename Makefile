gcr_location = deep-ego
model_name ?= clip-exercise-recognizer
version ?= latest
api_tag ?= gcr.io/${gcr_location}/${model_name}-api
dev_tag ?= gcr.io/${gcr_location}/${model_name}-dev
streamlit_tag ?=gcr.io/${gcr_location}/${model_name}-streamlit
model_version ?= $(shell cat .model_version)

build-api:
	echo 'Building API container.'
	docker build \
		-t $(api_tag):$(version) \
		-t $(api_tag):latest \
		-f Dockerfile.api .

build-dev:
	echo 'Building dev container.'
	docker build \
		-t $(dev_tag):$(version) \
		-t $(dev_tag):latest \
		-f Dockerfile.dev .

build-streamlit:
	echo 'Building streamlit container.'
	docker build \
		-t $(dev_tag):$(version) \
		-t $(dev_tag):latest \
		-f Dockerfile.dev .

api-cpu: build-api
	echo 'Starting API on port 8004. Running container on host network.'
	docker run \
		--name api \
		--net=host \
		--rm \
		-d \
		$(api_tag):$(version) \
		uvicorn src.api.main:app --host 0.0.0.0 --port 8000

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
		$(dev_tag):$(version) \
		jupyter lab --ip=0.0.0.0 --ServerApp.token='development' --ServerApp.password='development' --allow-root --no-browser

streamlit-cpu: build-api
	echo 'Starting API on port 8004. Running container on host network.'
	docker run \
		--name streamlit \
		--net=host \
		--rm \
		-d \
		$(api_tag):$(version) \
		streamlit run /workspace/src/streamlit/demo.py --server.port=8080

dev-cpu: build-dev
	echo 'Starting dev container in interactive shell mode.'
	docker run \
		--name dev \
		--net=host \
		-it \
		-d \
		--rm \
		-v `pwd`:/workspace \
		$(dev_tag):$(version) \
		jupyter lab --ip=0.0.0.0 --ServerApp.token='development' --ServerApp.password='development' --allow-root --no-browser

serve-cpu: streamlit-cpu api-cpu
	echo 'Waiting 30 seconds for services to fully start.'
	sleep 30

	echo 'Printing logs from API container.'
	docker logs api
