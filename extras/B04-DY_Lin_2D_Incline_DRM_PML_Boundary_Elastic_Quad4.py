"""
"""
import numpy as np
from Core import SeismoVLAB as SVL

#Model Options
SVL.Options['file'] = 'Performance_B04'
SVL.Options['numbering'] = 'Plain'
SVL.Options['nparts'] = 2
SVL.Options['dimension'] = 2

Lx = 140.0
Lz = 70.0
dh = 2.5

attributes = {
    'ne': [int(Lx/dh), int(Lz/dh)],
    'ndof': 2, 
    'P0': [-Lx/2, -Lz], 
    'P1': [ Lx/2, -Lz],
    'P2': [-Lx/2, 0.0],
    'class': 'LIN2DQUAD4',
    'elems': 'QUAD4',
    'attributes': {'th': 1.00, 'rule': 'Gauss','np': 4, 'material': 1}
}

Soil = SVL.makeDomainArea(attributes)

Lx = 160.0
Lz = 80.0
L  = 10.0

attributes = {
    'ne': [int(Lx/dh), int(Lz/dh)],
    'ndof': 5, 
    'P0': [-Lx/2, -Lz], 
    'P1': [ Lx/2, -Lz],
    'P2': [-Lx/2, 0.0],
    'class': 'PML2DQUAD4',
    'elems': 'QUAD4',
    'attributes': {'th': 1.00, 'n': 2.00, 'L': L, 'R': 1.000000E-03, 'x0': [], 'npml': [], 'rule': 'Gauss','np': 4, 'material': 1}
}

x0 = np.array([0.0,0.0])
xl = np.array([70.0, 70.0])

PML = SVL.setPMLDomain(attributes, x0, xl)

Soil = SVL.mergeDomain(Soil, PML)

SVL.setRestrains(Soil, dof=[1,2], bc=['bottom','left','right'])

#Find DRM Nodes and Elements
x0 = np.array([ 0.0, 0.0])
xl = np.array([50.1, 50.0])
SVL.setDRMDomain(Soil, x0, xl)

#The Domain Reduction Information 
DRM = {
    'theta': 15.0, 
    'phi': 0.0, 
    'x0': [0.0, 0.0], 
    'wave': 'SV',
    'field': 'VEL',
    'filename': 'Signal.txt',
    'dt': 0.004,
    'Ts': 2.5, 
    't': [], 
    'signal': [], 
    'Interior': Soil['DRM']['Interior'], 
    'Exterior': Soil['DRM']['Exterior'], 
    'Elements': Soil['DRM']['Elements']
}

#Create a Ricker signal for DRM
options = {'to': 0.75, 'f0': 2.0, 'dt': DRM['dt'], 'Ap': 0.1, 'Ts': DRM['Ts']}
DRM['t'], DRM['signal'] = SVL.Ricker(options, 'VEL')

SVL.WritePlaneWaveFile(DRM)

#Half-Space Parameters
Vs = 200.0
nu = 0.250
rho = 2000.0
Vp  = Vs*np.sqrt(2.0*(1.0 - nu)/(1.0 - 2.0*nu))

#Surface control points for recorders
xp = np.array([[-40.0, 0.0], [0.0,0.0], [40.0, 0.0]])
cPoints = SVL.Coords2Tag(Soil, xp, 1E-3)

#Create Material
SVL.addMaterial(tag=1, name='Elastic2DPlaneStrain', attributes={'E': 2.0*(1 + nu)*rho*Vs**2, 'nu': nu, 'rho': rho})

#Create Nodes
SVL.Entities['Nodes'] = Soil['Nodes']

#Create Constraints
SVL.Entities['Constraints'] = Soil['Constraints']

#Create Element
SVL.Entities['Elements'] = Soil['Elements']

#Create function
SVL.addFunction(tag=1, name='TimeSeries', attributes={'material': [1], 'layer': [0.0], 'file': DRM['filename'], 'x0': [0.0, 0.0], 'df': 0.2, 'CutOffFrequency': 15.0, 'option': 'SV', 'theta': 15.0, 'phi': 0.0})

#Create DRM load
SVL.addLoad(tag=1, name='ElementLoad', attributes={'fun': 1, 'type': 'PlaneWave', 'list': DRM['Elements']})

#Create a Combination
SVL.addCombinationCase(tag=1, name='PlaneWaveDRM', attributes={'load': [1], 'factor': [1.0]})

#Create Recorder
SVL.addRecorder(tag=1, attributes={'name': 'PARAVIEW', 'file': 'Animation.out', 'ndps': 8, 'nsamp': 5})
SVL.addRecorder(tag=2, attributes={'name': 'NODE', 'file': 'DispControlPoints.out', 'ndps': 8, 'resp': 'disp', 'list': cPoints})
SVL.addRecorder(tag=3, attributes={'name': 'NODE', 'file': 'VelsControlPoints.out', 'ndps': 8, 'resp': 'vel', 'list':  cPoints})
SVL.addRecorder(tag=4, attributes={'name': 'NODE', 'file': 'AccelControlPoints.out', 'ndps': 8, 'resp': 'accel', 'list':  cPoints})

#Creates the simulation
SVL.addAnalysis(tag=1, attributes={'name': 'Dynamic', 'nt': len(DRM['t'])})
SVL.addAlgorithm(tag=1, attributes={'name': 'Linear', 'nstep': 1})
SVL.addIntegrator(tag=1, attributes={'name': 'Newmark', 'dt': DRM['dt']})
SVL.addSolver(tag=1, attributes={'name': 'MUMPS', 'option': 'SYM', 'update': 'OFF'})
SVL.addSimulation(tag=1, combo=1, attributes={'analysis': 1, 'algorithm': 1, 'integrator': 1, 'solver': 1})

#Generate the SVL Run-Analysis Files
SVL.CreateRunAnalysisFiles(plot=True)
