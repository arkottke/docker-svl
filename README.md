# docker-svl

Docker contianer for Seismo-VLAB using OpenMPI

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

## Running code on Stampede2

Need to get onto a compute node. For interactive sessions, use `idev`. Once on the node:
```
Load singularity module
$ module load tacc-singularity

Change to $SCRATCH directory so containers do not go over your $HOME quota
$ cd $SCRATCH

Pull container
$ singularity pull docker://arkottke/tacc-svl-openmpi

Run container sequentially
$ ibrun -n 1 singularity run tacc-svl-openmpi_latest.sif COMMAND

Run container distributed
$ ibrun singularity run tacc-svl-openmpi_latest.sif COMMAND
```

To run `B04-DY_Lin_2D_Incline_DRM_PML_Boundary_Elastic_Quad4.py`
```
# Generate the DRM
c455-022[knl](1010)$ singularity run tacc-svl-openmpi_latest.sif \
    python3 B04-DY_Lin_2D_Incline_DRM_PML_Boundary_Elastic_Quad4.py
# Solve the problem
c455-022[knl](1013)$ singularity run tacc-svl-openmpi_latest.sif \
    mpirun -np 2 /home/svl/SVL/02-Run_Process/SeismoVLAB.exe \
        -dir '/scratch/04072/arkottke/svl/Partition' \
        -file 'Performance_B04.1.$.json'
```

For more information on TACC containers see [Containers@TACC](https://containers-at-tacc.readthedocs.io/en/latest/index.html) and [TACC Github](https://github.com/TACC/tacc-containers).
