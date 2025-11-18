import numpy as np
import pandas as pd
from Functions.projectsTable import getProject
import Functions.tableauMaker as tableauMaker

# Teableau is an numpy array
# is max is a boolean
def simplex(tableau, isMax):
    # work in float to avoid integer division and allow infinities
    tableau = tableau.astype(float, copy=True)
    nrow, ncol = tableau.shape
    verbose = []
    while (1):
        objRow = tableau[-1, :]

        # no more negatives in objective coefficients (exclude RHS)
        if np.all(objRow[:-1] >= 0): break
        pc = np.argmin(objRow[:-1])  # most negative coefficient (exclude RHS)

        # denominators is the row of the pivot col
        denom = tableau[:-1, pc]

        # get rhs
        rhs = tableau[:-1, -1]
        valid = denom > 0
        if (not np.any(valid)): # if all values are non positive
            return "Unbounded Error"
        
        testRatios = np.full(denom.shape, np.inf, dtype=float) # make np.arr thats full of inf thats the same size as denom
        testRatios[valid] = rhs[valid] / denom[valid] # for all valid numbers, do rhs/denom

        # .argmin() gets index of smallest number
        pr = np.argmin(testRatios)

        # pivot element and normalization of pivotrow
        pe = tableau[pr, pc]
        nPr = tableau[pr, :] / pe
        tableau[pr, :] = nPr
        for i in range(nrow):
            if (i != pr):
                tableau[i, :] = tableau[i, :] - (tableau[pr, :] * tableau[i, pc])

        # ADD TABLEAU AND BASIC SOLUTION EVERY ITERATION
        verbose.append([tableau.copy(), basicSol(tableau, isMax, nrow, ncol).copy()])
    
    finalTableau = tableau
    basicSolution = basicSol(finalTableau, isMax, nrow, ncol)
    Z = basicSolution[len(basicSolution)-1]
    return {
        "Final tableau": finalTableau,
        "Basic Solution": basicSolution,
        "Z": Z,
        "Verbose" : verbose
    }

def basicSol(tableau, isMax, nrow, ncol):
    # Extract basic variable values from final tableau
    # Identify columns that are unit vectors and take RHS at the 1's row
    if isMax == False:
        # For minimization last row entries
        return [tableau[nrow-1, :ncol-1], tableau[nrow-1, ncol-1]]

    baSo = []
    # for all columns
    for i in range(ncol-1): 
        # get column slice
        col = tableau[:, i] 
        # get column where there is exactly 1 non zero element
        if (col != 0).sum() == 1:
            r = np.where(col == 1)[0][0]
            baSo.append(tableau[r,-1]/tableau[r,i])
        else:
            baSo.append(0)
    return baSo

def expensesSummary(projects, basicSolution):
    
    newDf = pd.DataFrame(columns=['Project', 'Quantity', 'Total_Cost'])
    j = 0
    # 23 where the project count starts
    for i in range(23,len(basicSolution[0])-1):
        project_name = projects[j]
        j+=1
        project_data = getProject(project_name)
        quantity = basicSolution[0][i]
        total_cost = quantity * project_data[0]

        # Create new row as DataFrame
        new_row = pd.DataFrame({
            'Project': [project_name],
            'Quantity': [quantity],
            'Total_Cost': [total_cost]
        })
        # Concatenate properly
        newDf = pd.concat([newDf, new_row], ignore_index=True)
    return newDf

# projs = ['Boiler Retrofit', 'Traffic Signal/Flow Upgrade', 'Low-Emission Stove Program', 'Industrial Scrubbers', 'Reforestation (acre-package)', 'Agricultural Methane Reduction', 'Clean Cookstove & Fuel Switching (community scale)', 'Biochar for soils (per project unit)', 'Industrial VOC', 'Wetlands restoration', 'Household LPG conversion program', 'Industrial process change', 'Behavioral demand-reduction program']
# pop = tableauMaker.populateProjects(projs)
# ans = tableauMaker.systemsLinearConstructor(pop, [1000, 35, 25, 20, 60, 45, 80, 12, 6, 10])
# ans = tableauMaker.makeTableau(ans, False)

# ans = simplex(ans, False)
# print((ans["Basic Solution"][0]))
# print(expensesSummary(projs, ans["Basic Solution"]))