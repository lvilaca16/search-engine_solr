# Makefile
SHELL := /bin/bash

.PHONY: help
help:
	@echo "Commands:"
	@echo "style       : runs style formatting."
	@echo "down        : stops all running services, removes containers and volumes."
	@echo "up          : start Docker daemon and Solr."
	@echo "schema      : update schema using docker/data/schema.json."
	@echo "populate    : populate Solr using docker/data/data.json."
	@echo "create_core : populate Solr using docker/data/data.json."
	@echo "trec_eval   : download trec_eval source code and compile it."

.PHONY: style
style:
	isort src scripts --atomic
	black -l 100 src scripts
	flake8 src scripts

.PHONY: down
down:
	docker compose -f docker/docker-compose.yml down --remove-orphans -v

.PHONY: up
up:
	docker compose -f docker/docker-compose.yml up -d --remove-orphans

.PHONY: schema
schema:
	curl -X POST \
		-H 'Content-type:application/json' \
		--data-binary "@./docker/data/schema.json" \
		http://localhost:8983/solr/cfdata/schema

.PHONY: populate
populate:
	python scripts/preprocess.py --config_path config/config.json
	docker exec -it solr bin/solr post -c cfdata /data/data.json

.PHONY: create_core
create_core:
	docker exec -it solr bin/solr create_core -c cfdata

.PHONY: trec_eval
trec_eval:
	git clone https://github.com/usnistgov/trec_eval.git scripts/trec_eval
	cd scripts/trec_eval && make
	cd ../..
