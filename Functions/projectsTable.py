"""
INCLUDES PROJECTS LIST AND HOW TO GET THE PROJECT'S VALUES
"""
import pandas as pd

ProjectsList = pd.DataFrame({
  "ProjectNames" : ["Large Solar Park","Small Solar Installations","Wind Farm","Gas-to-renewables conversion","Boiler Retrofit","Catalytic Converters for Buses","Diesel Bus Replacement","Traffic Signal/Flow Upgrade","Low-Emission Stove Program","Residential Insulation/Efficiency", "Industrial Scrubbers","Waste Methane Capture System","Landfill Gas-to-energy","Reforestation (acre-package)","Urban Tree Canopy Program (street trees)","Industrial Energy Efficiency Retrofit","Natural Gas Leak Repair","Agricultural Methane Reduction","Clean Cookstove & Fuel Switching (community scale)","Rail Electrification", "EV Charging Infrastructure","Biochar for soils (per project unit)","Industrial VOC","Heavy-Duty Truck Retrofit","Port/Harbor Electrification","Black Carbon reduction","Wetlands restoration","Household LPG conversion program","Industrial process change","Behavioral demand-reduction program"],
  "Cost" : [4000,1200,3800,3200,1400,2600,5000,1000,180,900,4200,3600,3400,220,300,1600,1800,2800,450,6000,2200,1400,2600,4200,4800,600,1800,700,5000,400],
  "CO2" : [60,18,55,25,20,30,48,12,2,15,6,28,24,3.5,4.2,22,10,8,3.2,80,20,6,2,36,28,1.8,10,2.5,3,9],
  "NO" : [0,0,0,1,0.9,2.8,3.2,0.6,0.02,0.1,0.4,0.2,0.15,0.04,0.06,0.5,0.05,0.02,0.04,2,0.3,0.01,0.01,2.2,1.9,0.02,0.03,0.03,0.02,0.4],
  "SO2" : [0,0,0,0.2,0.4,0.6,0.9,0.1,0.01,0.05,6,0.1,0.05,0.02,0.01,0.3,0.01,0.01,0.02,0.4,0.05,0,0,0.6,0.8,0.01,0.02,0.01,0.01,0.05],
  "PM2.5" : [0,0,0,0.1,0.2,0.8,1,0.4,0.7,0.05,0.4,0.05,0.03,0.01,0.03,0.15,0.01,0.02,0.9,1.2,0.1,0.01,0,0.6,0.7,0.6,0.02,0.4,0,0.05],
  "CH4" : [0,0,0,1.5,0.1,0,0,0.05,0,0.02,0,8,6.5,0.8,0.6,0.2,4,7.2,0.1,0,0,2.5,0,0,0,0.05,3.2,0.05,0,0.01],
  "VOC" : [0,0,0,0.5,0.05,0.5,0.7,0.2,0.01,0.02,0.1,0.2,0.1,0.03,0.02,0.1,0.02,0.05,0.02,0.6,0.05,0.01,6.5,0.3,0.2,0.01,0.01,0.02,0,0.3],
  "CO" : [0,0,0,2,1.2,5,6,3,1.5,0.5,0.6,0.1,0.05,0.1,0.15,1,0.02,0.02,2,10,0.5,0.01,0.1,4.2,3.6,1,0.05,1.2,0,2.5],
  "NH3" : [0,0,0,0.05,0.02,0.01,0.02,0.02,0.03,0,0.01,0,0,0.01,0.005,0.01,0.02,0.1,0.05,0.02,0.01,0.2,0,0.01,0.01,0.02,0.15,0.03,0,0.01],
  "BC" : [0,0,0,0.01,0.01,0.05,0.08,0.02,0.2,0,0.01,0,0,0.005,0.02,0.01,0,0,0.25,0.1,0.01,0,0,0.04,0.03,0.9,0.02,0.1,0,0.01],
  "N2O" : [0,0,0,0.3,0.05,0.02,0.03,0.01,0,0.01,0,0.05,0.03,0.005,0.002,0.03,0.01,0.05,0,0.05,0.01,0.02,0,0.02,0.02,0,0.04,0,1.5,0.01],  
})


def getProject(projectName:str) -> list:
  # gets the whole row of the given projectName
  row = ProjectsList.loc[ProjectsList["ProjectNames"] == projectName]
  # removes the column name project names, and gets the integer values of the row then makes a list from them
  return row.drop(columns=["ProjectNames"]).iloc[0].tolist()