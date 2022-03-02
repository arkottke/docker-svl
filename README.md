# docker-svl

Docker contianer for Seismo-VLAB

Most of the important libraries are installed with the `PETSc` installer

## Running code locally

Docker compose recipes are used to help with the building and testing. To test the bulid execute:
```
$ make test
```
This build the image, and then run one of the examples.

If you want an interactive session, it can be started with:
```
$ make run
```
This will start and interactive session and the local `data` directory will be mapped to the svl home directory. For example,
```
~$ cd data
~/data$ python3 B04-DY_Lin_2D_Incline_DRM_PML_Boundary_Elastic_Quad4.py
~/data$ mpirun -np 2 /home/svl/SVL/02-Run_Process/SeismoVLAB.exe -dir '/home/svl/data/Partition' -file 'Performance_B04.1.$.json'
```
Note that currently *does not work*. It reports:
```
/opt/intel/impi/2019.7.217/intel64/bin/mpirun: 2: [: unexpected operator
```

## Running code on Stampede2

Need to get onto a compute node. For interactive sessions, use `idev`. Once on the node:
```
Load singularity module
$ module load tacc-singularity

Change to $SCRATCH directory so containers do not go over your $HOME quota
$ cd $SCRATCH

Pull container
$ singularity pull docker://arkottke/tacc-svl

Run container sequentially
$ ibrun -n 1 singularity run tacc-svl_latest.sif PROBLEM.py

Run container distributed
$ ibrun singularity run tacc-svl_latest.sif PROBLEM.py
```

For more information on TACC containers see [Containers@TACC](https://containers-at-tacc.readthedocs.io/en/latest/index.html).

## Issues

- Why doesn't the petsc build install binaries for mpmetis?
- There is a change in the variables in future versions of petsc; `PETSC_COMPILER` is renamed
