import os
from os import listdir
from os.path import isdir, isfile, join
import sys

if len(sys.argv) <3:
    print("BASEDIR and country should be set")
    exit(1)
basedir = sys.argv[1]
country  = sys.argv[2]
path = basedir + "/s/synthea/build/resources/main/modules/"
files = [f for f in listdir(path) if isfile(join(path, f))]
# add some extra running types
modules=[]
#modules.append('*')
#modules.append('cancer*')
for file in files:
    modules.append(os.path.splitext(file)[0])
# remove all USA veteran modules
modules = [x for x in modules if not 'veteran' in x]
print(modules)

# open file for writing markup file
os.mkdir(basedir + '/s/synthea/output')
os.chdir(basedir + '/s/synthea/output')
file = open("README.md","w") 
file.write("# " + country + " Download Page #\n")
file.write("You can download files by selecting the link\n\n")

for module in modules:
    # cleanup previous synthea run
    os.chdir(basedir + '/s/synthea')
    if (isdir('output')):
        if (isdir('output/csv')):
            filesToRemove = [f for f in os.listdir('output/csv')]
            for f in filesToRemove:
                os.remove(os.path.join('output/csv', f))
        if (isdir('output/fhir')):
            filesToRemove = [f for f in os.listdir('output/fhir')]
            for f in filesToRemove:
                os.remove(os.path.join('output/fhir', f))
    # run synthea
    os.system("./run_synthea -p 100 -m " + module + ' Uusimaa')
    # run synthea->omop 5.3.1
    os.chdir(basedir + '/s/ETL-Synthea-Python/python_etl')
    #export CDM_VERSION=531
    os.system("python synthea_omop.py")
    # run synthea->omop 6
    #export CDM_VERSION=6
    #cd $BASEDIR/s/ETL-Synthea-Python/python_etl
    #python synthea_omop.py
    # zip up omop output
    os.chdir(basedir + '/s/ETL-Synthea-Python/output')
    os.system("zip ../" + module + "_omop_531.zip *.csv")
    os.system("zip ../" + module + "_omop_6.zip *.csv")
    # zip up synthea output
    os.chdir(basedir + '/s/synthea/output/csv')
    os.system("zip ../" + module + "_synthea_csv.zip *.csv")
    os.chdir(basedir + '/s/synthea/output/fhir')
    os.system("zip ../" + module + "_synthea_fhir.zip *.csv")
    # write the links for this module
    synthea_fhir = "[[synthea fhir](https://github.com/science-automation/healthcare-europe-sample/raw/" + country + "/" + country + "/" + module + "_synthea_fhir.zip)]"
    synthea_csv = "[[synthea csv](https://github.com/science-automation/healthcare-europe-sample/raw/" + country + "/" + country + "/" + module + "_synthea_csv.zip)]"
    omop_cdm531 = "[[OMOP 5.3.1](https://github.com/science-automation/healthcare-europe-sample/raw/" + country + "/" + country + "/" + module + "_omop_531.zip)]"
    omop_cdm6 = "[[OMOP 6](https://github.com/science-automation/healthcare-europe-sample/raw/" + country + "/" + country "/" + module + "_omop_6.zip)]"
    file.write(module + ": " + synthea_fhir + synthea_csv + omop_cdm531 + omop_cdm6 + "\n\n")
file.close()
