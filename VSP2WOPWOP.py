# VSP2WOPWOP Main Script

#   Author: Daniel Weitsman

#   This is the main script which calls on and coordinates the executes of all the functions comprising the program.
#   There really shouldn't be a need to edit this script. If the code is ran in a python IDE three dictionaries, titled geomParams,XsecPolar,loadParams
#   will be returned these contain the analyzed geomtric parameters of the blades, the lift curve characteristics, and the aerodynamic loading/performance information, respectively.

#%%

from input import UserIn
import os
from shutil import rmtree
from functions.DegenGeom import ParseDegenGeom
from functions.GeomProcess import geomProcess
from functions.polarRead import polarRead
from functions.loadingHover import loadingHover
from functions.loadingFF import loadingFF
from functions.GeomPatchFileWrite import GeomPatchFileWrite
from functions.ConstantLoadingPatchFileWrite import ConstantLoadingPatchFileWrite
from functions.PeriodicLoadingPatchFileWrite import PeriodicLoadingPatchFileWrite
from functions.CompactGeomPatchFileWrite import CompactGeomPatchFileWrite
from functions.nml_write import nml_write
from functions.caseFile_write import caseFile_write

#%%

def main():

    if os.path.exists(UserIn['dirPatchFile']) == 0:
        os.mkdir(UserIn['dirPatchFile'])

    MainDict = {}
    loadParams = {}
    XsecPolar = {}
    globalFolder = []
    
    for i, dataFileName in enumerate(UserIn['dataFileName']):

        [dataSorted, indHeader] = ParseDegenGeom(UserIn['dirDataFile'],dataFileName)

        geomParams = geomProcess(dataSorted,indHeader,UserIn['loadPos'],UserIn['Nb'])

        dirSaveFile = os.path.abspath(os.path.expanduser(UserIn['dirPatchFile'] + '/' + dataFileName[:-4]))

        if i == 0:
            for ii, n in enumerate(UserIn['omega']):
                polarReadOut = polarRead(UserIn, ii)
                XsecPolar = {**XsecPolar, **{str(round(n)) + 'RPM': polarReadOut}}

        if os.path.exists(dirSaveFile) == 1:
            rmtree(dirSaveFile)
        os.mkdir(dirSaveFile)

#   Design Mode: Single loading condition per geometry
        if UserIn['OperMode'] == 1:

            GeomPatchFileWrite(UserIn['geomFileName'], geomParams,dirSaveFile)
            CompactGeomPatchFileWrite(UserIn['compactGeomFileName'], geomParams['nXsecs'], geomParams['liftLineCoord'],dirSaveFile)

            if UserIn['T'] is list:
                T = UserIn['T'][i]
            else:
                T = UserIn['T']

            if UserIn['Vx'] == 0:
                loadParams = loadingHover(UserIn, geomParams, XsecPolar[list(XsecPolar.keys())[i]], T, UserIn['omega'][i])
                ConstantLoadingPatchFileWrite(UserIn['loadingFileName'], loadParams, geomParams['nXsecs'],dirSaveFile)
            else:
                loadParams = loadingFF(UserIn, geomParams, XsecPolar[list(XsecPolar.keys())[i]], T, UserIn['omega'][i])
                PeriodicLoadingPatchFileWrite(UserIn['loadingFileName'], loadParams, geomParams['nXsecs'], UserIn['omega'][i],dirSaveFile)

            if UserIn['nmlWrite'] ==1:
                nml_write(UserIn,loadParams,dirSaveFile,i)

            if UserIn['BBNoise'] == 1:
                from functions.PeggBBDataFileWrite import PeggBBDataFileWrite
                PeggBBDataFileWrite(UserIn['bbFileName'], geomParams, loadParams)

            globalFolder.append(dataFileName[:-4])
            if i == len(UserIn['dataFileName']):
                caseFile_write(globalFolder, UserIn['NmlFileName'], UserIn['dirPatchFile'])

#   Analysis Mode: Multiple loading condition per geometry
        if UserIn['OperMode'] == 2:

            for ii,nThrust in enumerate(UserIn['T']):
                for iii, nVx in enumerate(UserIn['Vx']):
                    for iiii ,nOmega in enumerate(UserIn['omega']):

                        globalFolderName = '{:.2e}'.format(nThrust)+'N_'+str(round(nVx*1.944))+'Kts_'+str(round(nOmega))+'RPM'
                        dirCaseFile = os.path.abspath(os.path.expanduser(dirSaveFile + '/' + globalFolderName))

                        if os.path.exists(dirCaseFile) == 1:
                            rmtree(dirCaseFile)
                        os.mkdir(dirCaseFile)

                        GeomPatchFileWrite(UserIn['geomFileName'], geomParams,dirCaseFile)
                        CompactGeomPatchFileWrite(UserIn['compactGeomFileName'], geomParams['nXsecs'], geomParams['liftLineCoord'],dirCaseFile)

                        if nVx == 0:
                            loadingOut = loadingHover(UserIn, geomParams, XsecPolar[list(XsecPolar.keys())[iiii]], nThrust,  nOmega)
                            ConstantLoadingPatchFileWrite(UserIn['loadingFileName'], loadingOut, geomParams['nXsecs'], dirCaseFile)
                        else:
                            loadingOut = loadingFF(UserIn, geomParams, XsecPolar[list(XsecPolar.keys())[iiii]], nThrust, nOmega, nVx,UserIn['Vz'][iii],UserIn['alphaShaft'][iii])
                            PeriodicLoadingPatchFileWrite(UserIn['loadingFileName'], loadingOut, geomParams['nXsecs'],nOmega,dirCaseFile)

                        if UserIn['nmlWrite'] == 1:
                            nml_write(UserIn,loadingOut,dirCaseFile,iiii)

                        if UserIn['BBNoise'] == 1:
                            from functions.PeggBBDataFileWrite import PeggBBDataFileWrite
                            PeggBBDataFileWrite(UserIn['bbFileName'], geomParams, loadingOut)

                        loadParams = {**loadParams,**{globalFolderName:loadingOut}}

                        globalFolder.append(globalFolderName)
            caseFile_write(globalFolder, UserIn['NmlFileName'], dirSaveFile)

        MainDict = {**MainDict ,**{'UserIn':UserIn,dataFileName[:-4]:{'geomParams':geomParams,'XsecPolar':XsecPolar,'loadParams':loadParams}}}


        if UserIn['savePickle'] == 1:
            import pickle
            with open(os.path.abspath(os.path.expanduser(UserIn['dirPatchFile']+os.path.sep+'MainDict.pkl')), "wb") as f:
                pickle.dump(MainDict, f)

        #Use the following command to load data
        #pickle.load(open("file.pkl", "rb"))

    return MainDict


if __name__ =='__main__':
    print(__name__)
    MainDict = main()
