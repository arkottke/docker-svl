FROM tacc/tacc-ubuntu18

# System dependencies based on https://seismovlab.com/documentation/linkDebian.html
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends apt-utils && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get upgrade --yes && \
	apt-get install --yes --no-install-recommends \
        bash \
        ca-certificates \
        g++ \
        gcc \
        gfortran \
        git \
        libatlas-base-dev \
        libblacs-mpi-dev \
        liblapack-dev \
        libmetis-dev \
        libmumps-5.1.2 \
        libomp-dev \
        libopenmpi-dev \
        libparmetis-dev \
        libptscotch-dev \
        libscotch-dev \
        make \
        metis \
        openmpi-bin \
        openmpi-common \
        petsc-dev \
        python3-distutils \
        python3-matplotlib \
        python3-numpy \
        python3-scipy \
        python3-tk \
        ssh \
        vim \
        wget \
        && \
    docker-clean


RUN mkdir /usr/local/eigen && \
    wget -nv -O - https://gitlab.com/libeigen/eigen/-/archive/3.3.9/eigen-3.3.9.tar.gz | \
        tar -xz --strip-components=1 -C /usr/local/eigen

WORKDIR /tmp

# Add a non-root user because MPI complains about root privledges
RUN groupadd -r svl && useradd -ms /bin/bash -g svl svl

RUN cd /tmp && \
    git clone https://github.com/SeismoVLAB/SVL && \
    cd SVL/02-Run_Process && \
    sed -i 's:^EIGEN_DIR =.*:EIGEN_DIR = /usr/local/eigen:' Makefile.mk && \
    make DEBUG=no && \
    mkdir -p /home/svl/SVL/02-Run_Process && \
    mv /tmp/SVL/01-Pre_Process /home/svl/SVL/01-Pre_Process && \
    mv /tmp/SVL/02-Run_Process/SeismoVLAB.exe /home/svl/SVL/02-Run_Process/SeismoVLAB.exe && \
    ln -s /usr/bin/mpmetis /home/svl/SVL/01-Pre_Process/Metis && \
    chown svl:svl -R /home/svl

# Add hello world
ADD extras/hello.c /tmp/hello.c
RUN mpicc /tmp/hello.c -o /usr/local/bin/hellow \
    && rm /tmp/hello.c \
    && docker-clean

USER svl
WORKDIR /home/svl

ENV PYTHONPATH=/home/svl/SVL/01-Pre_Process
ENV PYTHONIOENCODING=utf-8
ENV MPLBACKEND=Agg

# Import matplotlib the first time to build the font cache.
RUN python3 -c "import matplotlib.pyplot"

CMD /bin/bash
