#!/usr/bin/bash

python3 B04-DY_Lin_2D_Incline_DRM_PML_Boundary_Elastic_Quad4.py

mpirun -np 2 SeismoVLAB.exe \
    -dir '/home/svl/Partition' \
    -file 'Performance_B04.1.$.json'
