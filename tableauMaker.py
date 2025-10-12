"""
FUNCTION FOR MAKING A TABLEAU FROM THE LIST OF PROJECTS
FOR USE OF THE SIMPLEX METHOD
"""


import projectsTable
import SimplexSolver

from asyncio import constants
from pickle import FALSE, NONE, TRUE
from select import poll
import pandas as pd
import numpy as np

# take in a matrix FXNS
# and boolean isMax
def makeTableau(fxns, isMax):
    if (isMax == FALSE):
        fxns = fxns.T

    # gets row and col of functions matrix
    nrow, ncol = fxns.shape

    # col and row - 1 so it stays within bounds of the matrix
    # makes objective funcion Ax = Z to Z - Ax = 0
    fxns[nrow-1, :] = np.r_[-fxns[nrow-1, :ncol-1], 0]
    slacks = np.identity(nrow, dtype=int)
    
    # puts the slacks just before the matrix's last row and retuns that
    return np.hstack([fxns[:, :ncol-1], slacks, fxns[:, ncol-1:ncol]])

# Projects included is a np.array of all the projects the user will include
# PollutantsToReduce is a list of the pollutants that the user needs to reduce
def systemsLinearConstructor(projectsIncluded, pollutantsToReduce): 
    # get the transpose so each row represents values for each of the unknows
    projs = projectsIncluded.T

    nUnknowns = len(projs[0])

    # Add 1 to the first index of pollutants, this will be our Z
    constantsCol = [1] + pollutantsToReduce  # create new list with 1 prepended
    constantsCol = np.array(constantsCol)[:,None]  # convert to column vector 
    
    # adds constant vector to last column of projects matrix
    projs = np.hstack([projs,constantsCol])


    # make constraints where x <= 20
    # and convert it into -x >= -20 so all constraints are >=
    constraints = np.identity(nUnknowns, dtype=int)
    constraints = -constraints
    maxProjs = np.array([-20] * nUnknowns)[:,None]
    constraints = np.hstack([constraints,maxProjs])

    # add constraints to matrix
    projs = np.vstack([projs,constraints])

    projs = np.vstack([projs,projs[0]]) # put first row (objective fxn) to last row
    projs = projs[1:, :]                  # drop original first row
    

    # Convert cij >= minPollutant into cij <= minPollutant
    # if you are dealing with minimization since you know cij >= minPollutant
    return projs



# TEST CASE
projs = ["Boiler Retrofit", "Traffic Signal/Flow Upgrade", "Low-Emission Stove Program", "Industrial Scrubbers", "Reforestation (acre-package)","Agricultural Methane Reduction", "Clean Cookstove & Fuel Switching (community scale)", "Biochar for soils (per project unit)", "Industrial VOC", "Wetlands restoration", "Household LPG conversion program", "Industrial process change", "Behavioral demand-reduction program"]
projs2 = ["Large Solar Park","Small Solar Installations","Wind Farm", "Gas-to-renewables conversion","Boiler Retrofit","Catalytic Converters for Buses"]
projsInclude = np.zeros((len(projs),11))

for i in range(len(projs)):
    projsInclude[i] = projectsTable.getProject(projs[i])

# convert projects and pollutants into a systems of linear equation
ans = systemsLinearConstructor(projsInclude, [1000,35,25,20,60,45,80,12,6,10])
np.savetxt("/Users/yel/Desktop/Coding/CMSC_150_proj/PythonVer/InitialSystems.txt", ans, delimiter="\t", fmt="%.6g")

# make it into a tableau
ans = makeTableau(ans, FALSE)
np.savetxt("/Users/yel/Desktop/Coding/CMSC_150_proj/PythonVer/InitialTableau.txt", ans, delimiter=" ", fmt="%.6g")


ans = SimplexSolver.simplex(ans,FALSE)
with open("/Users/yel/Desktop/Coding/CMSC_150_proj/PythonVer/output.txt", "w") as f:
    f.write(f"{ans}:\n")
