IMAGE   ?= trojan3877/logsight:dev
CHART   ?= infra/helm/logsight
NAMESPACE ?= logsight

.PHONY: build
build:
	g++ -O3 -march=native -std=c++17 -fPIC -shared src/cpp/simd_tokenizer.cpp -o src/cpp/libtok.so
	python -m pip install -r requirements.txt

.PHONY: test
test: build
	coverage run -m pytest -q && coverage report -m

.PHONY: dev
dev: build
	uvicorn src.python.api:app --reload --port 9000

.PHONY: docker
docker:
	docker build -t $(IMAGE) .

.PHONY: helm-up
helm-up:
	helm upgrade --install logsight $(CHART) --namespace $(NAMESPACE) --create-namespace
