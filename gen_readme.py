# generate the README.md file
import os

file = open("README.md","w")
file.write("# Sample Healthcare Data #\n")
file.write("Sample healthcare data in format fhir, omop and synthea for all EU countries\n\n")

# list of countries to be processed
countries= {"BE": "Belgium", "BG": "Bulgaria", "CZ": "Czechia", "DK": "Denmark", "DE": "Germany", "EE": "Estonia", "IE": "Ireland", "GR": "Greece", "ES": "Spain", "FR": "France", "HR": "Hungary", "IT": "Italy", "CY": "Cyprus", "LV": "Latvia", "LT": "Lithuania", "LU": "Luxembourg", "HU": "Hungary", "MT": "Malta", "NL": "Netherlands", "AT": "Austria", "PL": "Poland", "PT": "Portugal", "RO": "Romania", "SI": "Slovenia", "SK": "Slovakia", "FI": "Finland", "SE": "Sweden", "NO": "Norway", "UK": "UnitedKingdom"}
for key,value in countries.iteritems():
    branch = "[ Download Page ](https://github.com/science-automation/healthcare-europe-sample/tree/" + key.lower() + ") "
    azurepipeline = "[![" + value + "](https://dev.azure.com/shambergerm/HealthcareEuropeSample/_apis/build/status/" + value + "?branchName=master)](https://dev.azure.com/shambergerm/HealthcareEuropeSample/_build/latest?definitionId=3&branchName=master)\n\n"
    file.write("**" + value + "**: " + branch + azurepipeline)

file.close()
