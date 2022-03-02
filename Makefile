build:
	docker compose build shell

run: build
	docker compose run --rm --entrypoint bash shell

test: build
	docker compose up --remove-orphans test

push: build
	docker tag tacc-svl-openmpi arkottke/tacc-svl-openmpi
	docker push arkottke/tacc-svl-openmpi:latest
