'''
VSP2WOPWOP User Input File

Author: Daniel Weitsman

This input file is used to configure the cases for which to generate the patch and functional data files. VSP2WOPWOP
supports any number of DegenGeom files operating at any number of loading conditions, which are specified in the
comma-delimitted lists below (dataFileNames, Vx, W, omega). A folder that corresponds to each DegenGeom file,
containing the patch and namelist files for each loading condition, will be generated in the user specified directory.
'''
# %%
'''Package import and directory setup'''
import os

dirPyScript = os.getcwd()

# Directory where the DegenGeom and airfoil polars are located, by default this is set to the location of the
# test case folder.
dirDataFile = '/Users/danielweitsman/Desktop/Masters_Research/OLS Validation for Forward Flight'

# %%
''''Patch file write directory setup'''

# Directory were you would like to write out the patch and functional data flies. By default this path is configured
# to be a separate folder in the 'dirDataFile'.
dirPatchFile = os.path.abspath(os.path.join(dirDataFile, 'test_10_5'))

#   Blade geometry patch file name (without the extension).
geomFileName = "Geom"

#   Loading functional data file name (without the extension).
loadingFileName = "Load"

# %%

# Names of DegenGeom files add as many geometry cases as you wish separated by commas.
dataFileNames = ["OLS_DegenGeom.csv"]

# Operational mode: set equal to one for design mode, which is ideal for geometric parametric studies, where each
# variant of the blade geometry geometry corresponds to a different operating condition. Set this quantity equal to
# two to run in analysis mode. The analysis mode is tailored for running operational condition sweeps on each blade
# geometry.
operMode = 1

# Set equal to one in order to save the main dictionary, which contains all the computed geometric and loading
# parameters for the case to a .pkl file. This file can be read using the following command: pickle.load(open(
# "file.pkl", "rb"))
savePickle = 0

#%%
'''Airfoil Cross Section Configuration'''

# Name of XFoil files containing the airfoil cross section polars. The number of files should correspond to the
# number of 'XsecLocation'.
airfoilPolarFileName = [['b540olsRe11E5.dat']]

#   Non-dimensional radial location of each airfoil cross section
XsecLocation = [0.182]

# Starting angle of attack over which to evaluate the lift curve slop (degrees). The airfoil properties must have
# been evaluated at this angle of attack.
aStart = 1

#   Range over which to evaluate to evaluate the lift curve slope (degrees).
aLength = 4

# Set equal to one for the airfoil polars to be plotted, along with the interval that the lift curve slope is evaluated.
check = 0

# %%
''' Operating condition configuration '''
# Set equal to 1 in order to perform a wind tunnel trim on rotor (no longitudinal and lateral flapping), otherwise if
# the blade pitch is fixed set equal to zero.
trim = 1

# Number of Blades
Nb = 2

#   Forward velocity, set to zero for hover, input as many comma-delimited forward flight velocities as you wish to be
# evaluated.
Vx = [37.02464]

#   Vertical climb velocity (m/s), set to positive for ascent and negative for descent
Vz = [0]

#   Shaft tilt angle (degrees), forward tilt is designated by a negative tilt angle
alphaShaft = [-2]

#   Set the gross weight of the aircraft (N). Add as many comma-delimited thrust conditions as you wish into the list.
# Separate functional data files will be written for each case. If you are running in the design mode ('OperMode' = 1),
# the length of this list should be equal to the number of geometric cases ('dataFileNames').
T = [974.9446]

# Populate this list with the rotational rates (rpm) of the rotor. If you are running in the design mode ('OperMode'
# = 1), the length of this list should be equal to the number of geometric cases ('dataFileNames').
omega = [2250]

#   Initial collective pitch setting (degrees) used for trimming the rotor. This is an arbitrary value that should be
# adjusted to achieve convergence by ensuring that the computed angles of attack along the blade span lie within the
# limits of the Xfoil polars.
thetaInit = 1

#   Position of loading line from the blade's leading edge as a percentage of the chord.
loadPos = 0.25

#   Set equal to 1 to include Pardtl's tip loss formulation, only applies to hovering rotors
tipLoss =1

# Density (kg/m^3)
rho = 1.225

# Speed of sound (m/s)
c = 340

#   Blade mass moment of inertia about the flap hinge (only required for forward flight).
Ib = 1/3*2.266*(0.958-0.17436)**3

#   Nondimensionalized rotating flap frequency, this quantity is dependent on the non-rotating natural frequency and
# hinge offset of the blade (only required for forward flight).
nuBeta = 1

# %%
'''Broadband noise analysis configuration '''

#   Set equal to '1' to conduct a broadband noise prediction,'0' otherwise.
BBNoiseFlag = 0

#   Broadband noise method, set equal to '1' for Pegg's and '2' for the BPM's method.
BBNoiseModel = 2

# %%
'''Namelist file configuration'''
#   Set equal to one in order to write out a namelist file for each case.
nmlWrite = 0

#   Name of the namelist file that will be the same for all cases.
NmlFileName = 'OLS.nam'

#%%
'''Observer namelist configuration'''
#   Duration of the case, expressed as shaft revolutions
nRev = 1

#   Set sample rate (Hz), preferably as a power of two.
nt = 2 ** 14

# Observer type set equal to '1' for a single observer, '2' for a rectangular observer grid, and '3' for a
# spherical grid. Then complete the respective section below.
obsType = 3

# %%
'''Single Observer'''
#   x-position (ahead of the rotor) of observer
xLoc = 0

#   y-position (to the side of the rotor) of observer
yLoc = 14.165447920000007

#   z-position (vertical) of observer
zLoc = 14.165447920000007

# %%
'''Rectangular Observer Grid'''
#   Number of observers along the x-direction (ahead of the rotor).
nbx = 1

#   Minimum x coordinate
xMin = 0

#   Maximum x coordinate
xMax = [0]

#   Number of observers along the y-direction (to the side of the rotor).
nby = 1

#   Minimum y coordinate
yMin = 14.165447920000007

#   Maximum y coordinate
yMax = [14.165447920000007]

#   Number of observers along the z-direction (normal to the rotor plane).
nbz = 3

#   Minimum z coordinate
zMin = -1.4888485708273682

#   Maximum z coordinate
zMax = [1.4888485708273682]

# %%
'''Spherical Observer Grid'''
#   Radial position of the observers from the rotor hub.
radius = [30.48]

#   Number of in-plane observers
nbTheta = 1

#   Minimum angle of in-plane observer (degrees)
thetaMin = 0

#   Maximum angle of in-plane observer (degrees)
thetaMax = 0

#   Number of observers outside of the rotor plane (degrees)
nbPsi = 4

#   Minimum inclination angle of the out-of-plane observers (degrees)
psiMin = -45

#   Maximum inclination angle of the out-of-plane observers (degrees)
psiMax = 0

# %% Packs user input parameters into a dictionary (no need to edit)
UserIn = {'dirDataFile': dirDataFile, 'OperMode': operMode, 'savePickle': savePickle, 'dataFileName': dataFileNames,
          'airfoilPolarFileName': airfoilPolarFileName, 'XsecLocation': XsecLocation,
          'aStart': aStart, 'aLength': aLength, 'check': check,'trim':trim, 'Nb': Nb, 'Vx': Vx, 'Vz': Vz, 'alphaShaft': alphaShaft,
          'omega': omega, 'T': T, 'thetaInit': thetaInit, 'loadPos': loadPos, 'tipLoss': tipLoss, 'rho': rho, 'c': c,
          'Ib': Ib, 'nuBeta': nuBeta, 'nmlWrite': nmlWrite, 'dirPatchFile': dirPatchFile,
          'geomFileName': geomFileName, 'loadingFileName': loadingFileName, 'BBNoiseModel':BBNoiseModel,
          'BBNoiseFlag': BBNoiseFlag, 'NmlFileName': NmlFileName, 'nRev': nRev, 'nt': nt, 'obsType': obsType, 'xLoc': xLoc,
          'yLoc': yLoc, 'zLoc': zLoc, 'nbx': nbx, 'nby': nby, 'nbz': nbz, 'xMin': xMin, 'yMin': yMin, 'zMin': zMin,
          'xMax': xMax, 'yMax': yMax, 'zMax': zMax, 'radius': radius, 'nbtheta': nbTheta,
          'thetamin': thetaMin, 'thetamax': thetaMax, 'nbpsi': nbPsi, 'psimin': psiMin, 'psimax': psiMax}
