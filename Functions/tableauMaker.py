"""
FUNCTION FOR MAKING A TABLEAU FROM THE LIST OF PROJECTS
FOR USE OF THE SIMPLEX METHOD
"""


import Functions.projectsTable as projectsTable
import numpy as np

# take in a matrix FXNS
# and boolean isMax
def makeTableau(fxns, isMax):
    if (isMax == False):
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


def populateProjects(projs):
    projsInclude = []
    nProjs = len(projs)
    for i in range(nProjs):
        projsInclude.append(projectsTable.getProject(projs[i]))
    projsInclude = np.array(projsInclude)
    return projsInclude
