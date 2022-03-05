ifndef MPI_ARCH
$(error The MPI_ARCH variable is missing.)
endif

ifeq ($(filter $(MPI_ARCH),intel openmpi),)
$(error The MPI_ARCH variable is invalid.)
endif

IMAGE := tacc-svl-$(MPI_ARCH)

build:
	$(info Make: Building "$(MPI_ARCH)" environment images.)
	@MPI_ARCH=$(MPI_ARCH) docker compose build shell

run: build
	$(info Make: Running "$(MPI_ARCH)" environment images.)
	@MPI_ARCH=$(MPI_ARCH) docker compose run --rm --entrypoint bash shell

test: build
	rm -rf data/{DRM,MatrixPattern.png,Paraview,Partition,Signal.txt,Solution}
	@MPI_ARCH=$(MPI_ARCH) docker compose up --remove-orphans test

push:
	$(info Make: Pushing "$(IMAGE)" tagged image.)
	@docker push $(IMAGE):latest

clean:
	@docker system prune --volumes --force

login:
	$(info Make: Login to Docker Hub.)
	@docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)
