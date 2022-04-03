# Container's default name
NAME=demo

# Docker image default name
IMAGE=$(NAME)

# Mount localfile system
LOCAL_OPTS=-v $(shell pwd):/opt/exchange_demo \
		   -e PYTHONPATH="/opt/exchange_demo:/opt/exchange_demo/lib" \
		   -e CI=false \
		   --cap-add IPC_LOCK

# Build image
.PHONY: build
build:
	@echo "--> Building $(NAME)"
	docker build -t $(IMAGE) .

# Runs tests
.PHONY: run
run:
	@echo "--> Running tests"
	behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results/ ./features
	@echo "--> Creating allure report"
	allure generate --clean reports/allure-results/ -o reports/allure-report/

# Stop container
.PHONY: stop
stop:
	@echo "--> Stopping $(NAME)"
	docker kill $(NAME) || true

# Remove container
.PHONY: rm
rm:
	@echo "--> Removing container $(NAME)"
	docker rm -f $(NAME) || true

# Run container and provide a Shell terminal for debugging
.PHONY: local
local:
	@echo "--> Starting $(NAME)"
	docker run $(LOCAL_OPTS) --name $(NAME) --env-file secrets.ini -it $(IMAGE) /bin/sh

# Local development
.PHONY: dev
dev: stop rm build local
