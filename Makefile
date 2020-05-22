.PHONY: setup test run

setup:
	@echo "Build da(s) imagem(ns) docker."
	cd projeto && docker-compose build api
	cd projeto && docker-compose build test

test:
	@echo "Roda os testes da aplicação."
	cd projeto && docker-compose up test

run:
	@echo "Inicializa aplicação."
	cd projeto && docker-compose up api
	cd projeto && docker-compose up mongodb
